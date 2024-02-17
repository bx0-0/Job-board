from django import forms
import django_filters
from . models import Job
from django.contrib.auth.models import User

class JobFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    published =  django_filters.DateFilter(lookup_expr='icontains',help_text="enter data like '25 Jan 2024' ")
    CreateBy = django_filters.ModelChoiceFilter(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Job
        fields = [ 'job_type', 'description', 'published', 'Vacancy', 'salary', 'category', 'experience','CreateBy' ]