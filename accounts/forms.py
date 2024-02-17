from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import profile
import magic


def check_mime_type(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read())
    return file_mime_type


def check_file_size(file):
    size = file.size
    max_allowed_size = 2048576
    if size > max_allowed_size:
        raise forms.ValidationError("File size must be less than or equal to 2MB")


class SignupForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r"^\+?201\d{8,11}$",
        message="Phone number must be entered in the format: '+201234567890'. Up to 13 digits allowed and only E.G phone accept.",
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        required=False,
    )  # Validators should be a list

    email = forms.EmailField(
        help_text="Only Gmail  accounts are allowed to register you can register without emil",
        required=False,
    )
    is_company = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("is_company",)
        widgets = {
            "is_company": forms.RadioSelect(
                choices=[(True, "Company"), (False, "Employee")]
            ),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        print(0)
        # If the email has changed, check if it exists in the database
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            print(2)
            raise ValidationError("email already exists")

        elif (
            "email" in self.changed_data
            and not User.objects.filter(email=email).exists()
        ):
            return email
        else:
            print(4)
            return self.instance.email


class ProfileForm(forms.ModelForm):
    ProfileImg = forms.FileField(
        help_text="if you are company  pleas put your company image", required=False
    )

    class Meta:
        model = profile
        fields = (
            "specialization",
            "phone_number",
            "city",
            "ProfileImg",
        )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user_profile = self.instance
        if user_profile and not user_profile.is_company:
            self.fields["cv"] = forms.FileField(required=False)
            self.fields["is_cv_public"] = forms.BooleanField(
                required=False,
                label="If you are nominated on our website to be in the top 10, you can choose this option to display your CV when someone clicks on your name in the top 10.",
                 widget=forms.RadioSelect(choices=[(True, 'public'), (False, 'private')]),initial=user_profile.is_cv_public,
            )
            
           

        else:
            self.fields.pop("cv", None)
            self.fields.pop("is_cv_public", None)

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if cv:
            check_file_size(cv)
            file_type = check_mime_type(cv)

            if file_type == "application/pdf":
                return cv

            else:
                raise forms.ValidationError("Invalid file type only pdf allowed")
