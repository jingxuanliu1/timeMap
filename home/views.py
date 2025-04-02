from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    template_data = {}
    template_data['title'] = 'TimeMap'
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    template_data = {}
    template_data['title'] = 'Register'
    template_data['form'] = form
    return render(request, 'home/register.html', {'template_data': template_data})

def friends(request):
    template_data = {}
    template_data['title'] = 'Friends'
    return render(request, 'home/friends.html', {'template_data': template_data})

def leaderboard(request):
    template_data = {}
    template_data['title'] = 'Leaderboard'
    return render(request, 'home/leaderboard.html', {'template_data': template_data})

def settings(request):
    template_data = {}
    template_data['title'] = 'Settings'
    return render(request, 'home/settings.html', {'template_data': template_data})