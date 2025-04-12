from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('settings/', views.profile_settings, name='settings'),
    path('', views.profile, name='profile'),
path('friends/', views.friend_list, name='friend_list'),
    path('friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friend_request/<int:request_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
]