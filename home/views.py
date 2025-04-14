from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from home.forms import CustomUserCreationForm


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data[('email')]
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('home.index')
        else:
            messages.error(request, 'There was an error with your registration. Please check your details.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'home/register.html', {
        'title': 'Register',
        'form': form
    })

def friends(request):
    template_data = {}
    template_data['title'] = 'Friends'
    return render(request, 'home/friends.html', {'template_data': template_data})

def leaderboard(request):
    template_data = {}
    template_data['title'] = 'Leaderboard'
    return render(request, 'home/leaderboard.html', {'template_data': template_data})

def settings(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access your settings.')
        return redirect('login')
    return render(request, 'home/settings.html', {'template_data': template_data})

def home(request):
    return render(request, 'home.html')