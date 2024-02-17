from . import views
from  django.urls import path

app_name= 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.Profile_Show, name='profile'),
    path('profile/edit/', views.ProfileEdit, name='profile_edit'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate_user'),
]