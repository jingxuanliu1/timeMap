from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('settings/', views.profile_settings, name='settings'),
    path('', views.profile, name='profile'),
]