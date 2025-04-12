from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile_settings(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, gmail=request.user.email or '')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profiles:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profiles/settings.html', {'form': form, 'title': 'Profile Settings'})


@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, gmail=request.user.email or '')

    context = {
        'title': 'Your Profile',
        'user': request.user,  # Make sure user is passed
        'profile': profile  # Make sure profile is passed
    }
    return render(request, 'profiles/profile.html', context)