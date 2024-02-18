from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Job
from .form import ApplyForm, AddNewJobForm
from django.conf import settings
from django.db import transaction
from .filters import JobFilter
# Create your views here.


def ShowJobsList(request):
    JobList = Job.objects.all().order_by('id')  # django models queryset
    #!apply my filter 
    my_filter = JobFilter(request.GET,queryset=JobList)
    
    JobList = my_filter.qs    
    paginator = Paginator(JobList, 3)  # show 3 content per page
    PageNumber = request.GET.get("page")  # get the number of page
    page_obj = paginator.get_page(PageNumber)  # this line complete the up  line
    context = {
        "jobs": page_obj,  # name of variable in  templates
        "my_filter": my_filter, 
    }

    return render(request, "Job/JobList.html", context)



@login_required
@transaction.atomic
def JobsDetails(request, slug):
    JobDetails = Job.objects.get(slug=slug)

    
    if request.method == "POST":
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.profile.cv :
                print('hello')
                MyForm = form.save(commit=False)
                MyForm.job = JobDetails
                cv =  request.user.profile.cv 
                MyForm.save()
                if MyForm:
                    send_applier_info_to_job_owner(request,JobDetails.CreateBy.email, MyForm,cv)
            else:
                messages.error(request, 'Please go to the profile editing page and upload your resume, as it will be directly uploaded.')
                return redirect('accounts:profile_edit')  
                    
    else:
        form = ApplyForm()

    context = {
        "job": JobDetails,
        "form": form,
    }

    return render(request, "Job/JobDetails.html", context)


@login_required
@user_passes_test(lambda x: x.profile.is_company)
def AddNewJob(request):
    if request.user.email:
        if request.method == "POST":
            form = AddNewJobForm(request.POST, request.FILES)

            MyForm = form.save(commit=False)

            MyForm.CreateBy = request.user

            MyForm.save()

            return redirect(reverse("jobs:jobs_details", kwargs={"slug": MyForm.slug}))

        else:
            form = AddNewJobForm()

    else:
        messages.info(
            request,
            message="Please go to  your edit profile and add email before creating job post",
        )
        form = ""
    context = {"form": form}
    return render(request, "Job/PostJob.html", context=context)



def send_applier_info_to_job_owner(request, job_owner_email, form,cv):
    print(cv)
    try:
        subject = "New application for your job"
        text_content =  f"""
        Hi,

        You have a new application for your job. Here are the details:

        
        Name: {form.name}
        Email: {form.mail}
        URL:   {form.url}
        CV: {cv}
        Additional Information: {form.info_for_applier}
        

        Please review the application and respond accordingly.</p>

        Thank you,fun  job
        """
        html_content = f"""
        <string>Hi,</string>

        <p>You have a new application for your job. Here are the details:</p>

        <ul>
            <li>Name: {form.name}</li>
            <li>Email: {form.mail}</li>
            <li>URL: <a href={form.url}>Applier website </a></li>
            <li>CV: {cv}</li>
            <li>Additional Information: {form.info_for_applier}</li>
        </ul>

        <p>Please review the application and respond accordingly.</p>

        <p>Thank you,<br>fun  job</p>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[job_owner_email],
        )

        if cv:
            path = cv.path
            email.attach_file(path)

        # إرفاق النص HTML بالبريد الإلكتروني
        email.attach_alternative(html_content, "text/html")

        email.send(fail_silently=False)
        
        messages.success(request, message="Email sent successfully thinks to use our site ")
        
    except Exception as e:  # noqa: F841
        form.delete() #لاحظ هنا ممكن  احذف الفورم  الي اتخزن  بالفعل في قاعدة البيانات  في حالة حدوث خطا    
        messages.error(request=request, message=f"Error sending please try again, {e}")