from . import views
from  django.urls import path

app_name= 'home'
urlpatterns = [
    path('', views.render_home ,name=''),
]