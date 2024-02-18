from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import ProfileForm, SignupForm, UserForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.dispatch import receiver
from .models import profile
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Create your views here.


@transaction.atomic
def signup(request):
    context = {}
    try:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                email = form.cleaned_data["email"]
                user.is_active = False if email else True
                user.email = email if email else user.email
                user.save()
                Phone_number = form.cleaned_data["phone_number"]
                is_company = form.cleaned_data["is_company"]
                user.profile.phone_number = Phone_number
                user.profile.is_company = is_company
                user.profile.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]

                if email:
                    generate_token_send_verification_email_and_accounts(
                        request, user, "singup", email
                    )
                else:
                    session_user = authenticate(username=username, password=password)
                    if session_user is not None:
                        login(request, session_user)
                        return redirect(reverse("accounts:profile_edit"))
        else:
            form = SignupForm()
        context = {"form": form}

    except Exception as e:
        messages.error(request, message=f"error occurred please try again {e}")
    return render(request, "registration/signup.html", context=context)


@transaction.atomic
def generate_token_send_verification_email_and_accounts(
    request, user, keword="", email=""
):
    # Generate token
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = (
        f"https://django-job-board-59na.onrender.com/accounts/activate/{uidb64}/{token}"
    )
    #!send email
    print(email)
    if keword == "singup" and email:
        try:
            message = f"""
                        Hi there,

                            Thank you for registering on our site. To activate your account, please click on the link below:

                            {activation_link}

                            If you have any questions, please don't hesitate to contact us.

                            Thank you,
                            Support Team
                        """
            subject = "Account verification"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,  #!from
                recipient_list=[email],  #! to
                fail_silently=False,
            )
            messages.success(
                request,
                message="we send you a verification email check  your inbox",
            )

        except TypeError as e:  # Catch the exception
            messages.error(request=request, message=f"Error occurred: {e}")
    else:
        try:
            message = f"""
                        Hi there,

                            Thank you for registering on our site. To activate your email, please click on the link below:

                            {activation_link}

                            If you have any questions, please don't hesitate to contact us.

                            Thank you,
                            Support Team
                        """
            subject = "Email verification"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,  #!from
                recipient_list=[user.profile.unconfirmed_email],  #! to
                fail_silently=False,
            )
            messages.success(
                request,
                message="please confirm your email  to show it here",
            )

        except TypeError as e:  # Catch the exception
            messages.error(request=request, message=f"Error occurred: {e}")


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            user.email = request.user.profile.unconfirmed_email
            request.user.profile.unconfirmed_email = ""
            request.user.profile.save()
            user.save()
        else:

            user.is_active = True
            user.save()
            print(user.email)
            login(request, user)
        return redirect(reverse("accounts:profile_edit"))

    return render(request, "registration/activate.html", context={})


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@login_required
def Profile_Show(request):
    context = {}
    try:
        profile_ = profile.objects.get(user=request.user)
        context = {
            "profile": profile_,
        }
    except Exception:
        messages.error(request, message="An error occurred")

    return render(request, "registration/profile.html", context=context)


@login_required
def ProfileEdit(request):
    try:
        user_profile, created = profile.objects.get_or_create(user=request.user)
        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(
                request.POST,
                request.FILES,
                instance=user_profile,
            )

            if user_form.is_valid() and profile_form.is_valid():
                email = User.objects.get(id=request.user.id).email
                user_form.save()
                MyProfileForm = profile_form.save(commit=False)
                if "is_cv_public" in request.POST:
                    is_cv_public = profile_form.cleaned_data["is_cv_public"]
                    request.user.profile.is_cv_public = is_cv_public
                    request.user.profile.save()

                if (
                    user_form.cleaned_data.get("email") != email
                    and "email" in user_form.changed_data
                ):
                    request.user.profile.unconfirmed_email = request.user.email
                    request.user.email = ""
                    request.user.profile.save()
                    request.user.save()
                    generate_token_send_verification_email_and_accounts(
                        request=request, user=request.user
                    )

                MyProfileForm.user = request.user
                MyProfileForm.save()  #!

                return redirect(reverse("accounts:profile"))
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=user_profile)

        context = {
            "UserForm": user_form,
            "ProfileForm": profile_form,
        }
    except Exception as e:
        messages.error(request, message=f"Error occurred  try please again, {e}")
        context = {}

    return render(request, "registration/profile_edit.html", context=context)
