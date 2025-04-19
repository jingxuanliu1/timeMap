from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('settings/', views.profile_settings, name='settings'),
    path('', views.current_user_profile, name='current_profile'),
    path('friends/', views.friend_list, name='friend_list'),
    path('friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friend_request/<int:request_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
    path('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),
    path('search/', views.search_users, name='search_users'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('preferences/', views.preferences, name='preferences'),
    path('<str:username>/', views.profile_view, name='profile'),
]