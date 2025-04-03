from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


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
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
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
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access your settings.')
        return redirect('login')

    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'profile_submit' in request.POST:
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home.settings')
    else:
        profile_form = UserProfileForm(instance=profile)

    template_data = {
        'title': 'Settings',
        'profile_form': profile_form,
    }
    return render(request, 'home/settings.html', {'template_data': template_data})