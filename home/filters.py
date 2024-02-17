import django_filters 
from job.models import Job 

class JobFilter(django_filters.FilterSet): 
    description = django_filters.CharFilter(lookup_expr='icontains') 
    location =  django_filters.CharFilter(lookup_expr='icontains')
    class Meta: 
        model = Job 

        fields = [ 'description', 'location','category' ] 