from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import os
from uuid import uuid4

# Create your models here.


def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)
    id = uuid4()
    return f"JobsImages/{id}{ext}"



class Job(models.Model):  # inherited from models.Model , classes equivalent tables
    CreateBy = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # not accept default = ''

    title = models.CharField(
        max_length=100, default=""
    )  # Create column title (charfield)
    location = models.CharField(max_length = 60,default="")
    
    Job_type = (
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
    )

    job_type = models.CharField(choices=Job_type, max_length=30, default=Job_type[0])

    description = models.TextField(default="")

    published = models.DateTimeField(auto_now=True)

    Vacancy = models.IntegerField(default=1)

    salary = models.PositiveIntegerField(default=100)

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE
    )  # one to many relationship relations between categories and jobs

    experience = models.PositiveBigIntegerField(default=0)

    img = models.ImageField(upload_to=GetImageUploadTo, default="")

    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.handle_image_upload()
        self.handle_slug_creation()
        return super().save(*args, **kwargs)

    def handle_image_upload(self):
        # to control new  images upload if old image is already existing delete it and replace with new image
        # if the object already exists and the image is updated
        if self.pk and Job.objects.get(pk=self.pk).img:
            old_img = Job.objects.get(pk=self.pk).img
            if os.path.isfile(old_img.path):
                os.remove(old_img.path)

    def handle_slug_creation(self):
        # to control slugs
        self.slug = slugify(self.title) + "-" + str(uuid4())

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self) -> str:
        return self.name


class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="")
    mail = models.EmailField(default="")
    url = models.URLField(default="")
    info_for_applier = models.TextField(max_length=300, default="")
    cv = models.FileField(default='', blank=True, null=True)

            

    def __str__(self):
        return self.name
