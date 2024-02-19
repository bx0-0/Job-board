import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cities_light.models import City

# Create your models here.


def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)
    id = uuid4()
    return f"profile/{id}{ext}"


def GetfileUploadTo(instance, cv):
    name, ext = os.path.splitext(cv)
    id = uuid4()

    return f"cvs/{id}{ext}"


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unconfirmed_email = models.EmailField(blank=True, null=True)
    is_company = models.BooleanField(default=True)
    ProfileImg = models.ImageField(upload_to=GetImageUploadTo, null=True, blank=True)
    cv = models.FileField(
        upload_to=GetfileUploadTo,
        null=True,
        blank=True,
        default="",
    )
    # --An optional phone number.
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_regex = RegexValidator(
        regex=r"^\+?201\d{8,11}$",
        message="Phone number must be entered in the format: '+201234567890'. Up to 13 digits allowed and only E.G phone accept.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    # create city
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    specialization = models.CharField(max_length=100, blank=True, null=True)

    is_cv_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        self.handle_image_upload()
        self.handle_cv_upload()

        return super().save(*args, **kwargs)

    def handle_image_upload(self):
        if self.ProfileImg:
            old_img = profile.objects.get(pk=self.pk).ProfileImg
            if (
                self.pk
                and profile.objects.get(pk=self.pk).ProfileImg
                and old_img != self.ProfileImg
            ):

                if os.path.isfile(old_img.path):
                    os.remove(old_img.path)

    def handle_cv_upload(self): 
        if self.cv:
            old_cv = profile.objects.get(pk=self.pk).cv
            if self.pk and profile.objects.get(pk=self.pk).cv and old_cv != self.cv:

                if os.path.isfile(old_cv.path):
                    os.remove(old_cv.path)
