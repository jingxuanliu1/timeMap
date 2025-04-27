from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from profiles.forms import CustomUserCreationForm
from profiles.models import UserProfile
from django.db import IntegrityError
from tasks.models import Task, Quote
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import requests
import os

def index(request):
    today = timezone.localdate()
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date=today
    ) if request.user.is_authenticated else []
    completed_count = tasks.filter(completed=True).count() if tasks else 0

    quote_data = None
    try:
        quote = Quote.objects.filter(fetched_date=today).first()
        if not quote:
            api_url = 'https://api.api-ninjas.com/v1/quotes'
            headers = {'X-Api-Key': os.getenv('QUOTES_API_KEY')}
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()[0]
                quote = Quote.objects.create(
                    quote=data['quote'],
                    author=data['author'],
                    category=data.get('category', ''),
                    fetched_date=today
                )
        if quote:
            quote_data = {
                'quote': quote.quote,
                'author': quote.author
            }
    except Exception as e:
        print(f"Error fetching quote: {e}")

    template_data = {
        'title': 'TimeMap',
        'tasks': tasks,
        'completed_count': completed_count,
        'today_date': today.strftime("%B %d, %Y"),
        'quote_data': quote_data
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
    return render(request, 'home/register.html', template_data)

def friends(request):
    template_data = {
        'title': 'Friends',
    }
    return render(request, 'home/friends.html', {'template_data': template_data})

@login_required
def leaderboard(request):
    user_profile = request.user.userprofile
    friends = user_profile.get_friends()
    users_to_rank = [user_profile.user] + [friend.user for friend in friends]

    leaderboard_data = []
    for user in users_to_rank:
        completed_count = Task.objects.filter(user=user, completed=True).count()
        leaderboard_data.append({
            'user': user,
            'profile': user.userprofile,
            'completed_count': completed_count,
            'is_current_user': user == request.user
        })

    leaderboard_data.sort(key=lambda x: x['completed_count'], reverse=True)

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
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access your settings.')
        return redirect('login')
    template_data = {
        'title': 'Settings',
    }
    return render(request, 'home/settings.html', {'template_data': template_data})

def home(request):
    return render(request, 'home.html')
