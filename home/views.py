from django.shortcuts import render
from job.models import Job
from job.models import Category
from .filters import JobFilter
from accounts.models import profile
from django.db.models import Count
# Create your views here.


def render_home(request):
    all_job = Job.objects.all()
    job_counts =  len(all_job)
    all_job = all_job[:6]
    categories = Category.objects.all()

    popular_categories = sorted(
        categories, key=lambda category: category.job_set.count(), reverse=True
    )[:8]
    filter = JobFilter(request.GET, queryset=Job.objects.all())

    all_job = sorted(filter.qs, key=lambda x: x.Vacancy, reverse=True)[:8]



    # Get all profiles of users who are not companies
    profiles = profile.objects.filter(is_company=False)

    # Annotate each profile with the sum of likes on all of their posts
    profiles = profiles.annotate(total_likes=Count('user__post__likes'))

    # Order the profiles by total likes
    top_10 = profiles.order_by('-total_likes')[:10]
    
    company_profiles = profile.objects.filter(is_company = True)
    company_profiles= company_profiles.annotate(total_jobs =Count('user__job'))
    
    top_10_company = company_profiles.order_by('-total_jobs')[:10]
    
    for i in  top_10:
        print(i)
    context = {
        'top_10_company':top_10_company,
        "top_10": top_10,
        "my_filter": filter,
        "categories": popular_categories,
        "jobs": all_job,
        'job_counts': job_counts,
       
    }

    return render(request, "home/home.html", context=context)
