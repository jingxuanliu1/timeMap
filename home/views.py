from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from profiles.forms import CustomUserCreationForm
from profiles.models import UserProfile
from django.db import IntegrityError
from tasks.models import Task

def index(request):
    tasks = Task.objects.filter(user=request.user) if request.user.is_authenticated else []
    completed_count = tasks.filter(completed=True).count() if tasks else 0
    template_data = {
        'title': 'TimeMap',
        'tasks': tasks,
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
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Account created for {username}! You are now logged in.')
                return redirect('home.index')
            except IntegrityError:
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            messages.error(request, 'There was an error with your registration. Please check your details.')
    else:
        form = CustomUserCreationForm()

    template_data = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'home/register.html', {'template_data': template_data})

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
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access your settings.')
        return redirect('login')
    template_data = {
        'title': 'Settings',
    }
    return render(request, 'home/settings.html', {'template_data': template_data})

def home(request):
    return render(request, 'home.html')
