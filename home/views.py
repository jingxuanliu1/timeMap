from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.models import UserProfile
from django.db import IntegrityError
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from profiles.forms import CustomUserCreationForm
from django.utils import timezone
from datetime import datetime

def index(request):
    today = timezone.localdate()  # Get today's date
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date=today
    ) if request.user.is_authenticated else []
    completed_count = tasks.filter(completed=True).count() if tasks else 0
    template_data = {
        'title': 'TimeMap',
        'tasks': tasks,
        'completed_count': completed_count,
        'today_date': today.strftime("%B %d, %Y")  # Format: "Month Day, Year"
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

@login_required
def leaderboard(request):
    # Get the current user's profile
    user_profile = request.user.userprofile

    # Get all friends (using your existing get_friends() method)
    friends = user_profile.get_friends()

    # Create list of users to rank (current user + friends)
    users_to_rank = [user_profile.user] + [friend.user for friend in friends]

    # Get completed task count for each user
    leaderboard_data = []
    for user in users_to_rank:
        completed_count = Task.objects.filter(user=user, completed=True).count()
        leaderboard_data.append({
            'user': user,
            'profile': user.userprofile,  # Access profile data
            'completed_count': completed_count,
            'is_current_user': user == request.user
        })

    # Sort by completed tasks (descending)
    leaderboard_data.sort(key=lambda x: x['completed_count'], reverse=True)

    # Add rank position (handling ties)
    if leaderboard_data:
        leaderboard_data[0]['rank'] = 1
        for i in range(1, len(leaderboard_data)):
            if leaderboard_data[i]['completed_count'] == leaderboard_data[i - 1]['completed_count']:
                leaderboard_data[i]['rank'] = leaderboard_data[i - 1]['rank']
            else:
                leaderboard_data[i]['rank'] = i + 1

    template_data = {
        'title': 'Leaderboard',
        'leaderboard': leaderboard_data,
        'has_friends': len(friends) > 0
    }
    return render(request, 'home/leaderboard.html', {'template_data': template_data})

def settings(request):
    # Your settings view logic here
    return render(request, 'home/settings.html', {'title': 'Settings'})