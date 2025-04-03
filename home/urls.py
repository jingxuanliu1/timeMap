from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('register', views.register, name='home.register'),
    path('friends', views.friends, name='home.friends'),
    path("leaderboard", views.leaderboard, name='home.leaderboard'),
    path('settings', views.settings, name='home.settings'),

]