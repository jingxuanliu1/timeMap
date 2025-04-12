from django.shortcuts import render
from django.contrib import messages
from profiles.forms import CustomUserCreationForm


def index(request):
    template_data = {
        'title': 'TimeMap',
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
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
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