from . import views
from  django.urls import path

app_name= 'job'
urlpatterns = [
    path('', views.ShowJobsList ,name=''),
    path('add', views.AddNewJob, name='AddNewJob'),
    path('<slug>/', views.JobsDetails, name='jobs_details'),
]