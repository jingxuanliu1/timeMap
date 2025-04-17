from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.forms import CustomUserCreationForm
from profiles.models import UserProfile
from django.db import IntegrityError
from tasks.models import Task


def index(request):
    tasks = Task.objects.filter(user=request.user) if request.user.is_authenticated else []
    completed_count = tasks.filter(completed=True).count() if tasks else 0
    template_data = {
        'title': 'TimeMap',
        'tasks' : tasks,
        'completed_count': completed_count,
    }
    return render(request, 'home/index.html', {'template_data': template_data})


def about(request):
    template_data = {
        'title': 'About TimeMap',
    }
    return render(request, 'home/about.html', {'template_data': template_data})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'home/register.html', {
        'template_data': {'title': 'Register', 'form': form,}})

def friends(request):
    template_data = {
        'title': 'Friends',
    }
    return render(request, 'home/friends.html', {'template_data': template_data})


def leaderboard(request):
    template_data = {
        'title': 'Leaderboard',
    }
    return render(request, 'home/leaderboard.html', {'template_data': template_data})
def settings(request):
    # Your settings view logic here
    return render(request, 'home/settings.html', {'title': 'Settings'})