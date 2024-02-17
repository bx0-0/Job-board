import django_filters
from django import forms
from . models import Category, Post
from django.db.models import Q

class PostFilter(django_filters.FilterSet):
    multi_name_fields = django_filters.CharFilter(method='filter_by_all_fields', label='Post Title or Description')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = Post
        fields = []

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(post_content__icontains=value)
        )
