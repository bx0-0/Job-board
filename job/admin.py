from django.contrib import admin

# Register your models here.
#Here we add any  models you Create  to appear to  us in  admin panel

from .models import Job , Category, Apply

admin.site.register(Job)

admin.site.register(Category)

admin.site.register(Apply)
