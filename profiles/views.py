from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import UserProfileForm
from .models import UserProfile, Friendship
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.models import User


@login_required
def profile_settings(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profiles:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profiles/settings.html', {
        'form': form,
        'title': 'Profile Settings'
    })


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    is_own_profile = (request.user == user)

    friendship_status = None
    request_id = None
    is_friend = False

    if not is_own_profile:
        current_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        is_friend = current_profile.is_friends_with(profile)
        friendship_status = current_profile.get_friendship_status(profile)

        if friendship_status == 'request_received':
            request_id = Friendship.objects.get(
                from_user=profile,
                to_user=current_profile
            ).id

    return render(request, 'profiles/profile.html', {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'friendship_status': friendship_status,
        'request_id': request_id,
        'is_friend': is_friend
    })


@login_required
def friend_list(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    query = request.GET.get('q', '')
    search_results = None

    if query:
        search_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id).select_related('userprofile')

    # Get friends list - now using the properly implemented get_friends()
    friend_profiles = profile.get_friends()
    friends_users = [friend_profile.user for friend_profile in friend_profiles]

    # Get pending requests
    sent_requests = Friendship.objects.filter(
        from_user=profile,
        accepted=False
    ).select_related('to_user__user')

    received_requests = Friendship.objects.filter(
        to_user=profile,
        accepted=False
    ).select_related('from_user__user')

    friend_requests_sent = [req.to_user.user for req in sent_requests]
    friend_requests_received = [req.from_user.user for req in received_requests]

    return render(request, 'profiles/friend_list.html', {
        'friends': friends_users,
        'pending_requests': received_requests,
        'friend_requests_sent': friend_requests_sent,
        'friend_requests_received': friend_requests_received,
        'search_results': search_results,
        'query': query
    })


@login_required
def send_friend_request(request, username):
    if request.method == 'POST':
        try:
            to_user = User.objects.get(username=username)
            to_profile = to_user.userprofile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "The user you're trying to add doesn't exist.")
            return redirect('profiles:friend_list')

        from_profile = request.user.userprofile

        if from_profile == to_profile:
            messages.error(request, "You cannot send a friend request to yourself.")
            return redirect('profiles:profile', username=username)

        status = from_profile.get_friendship_status(to_profile)

        if status == 'friends':
            messages.info(request, f"You are already friends with {username}.")
        elif status == 'request_sent':
            messages.warning(request, "Friend request already sent.")
        elif status == 'request_received':
            try:
                friendship = Friendship.objects.get(
                    from_user=to_profile,
                    to_user=from_profile
                )
                friendship.accepted = True
                friendship.save()
                messages.success(request, f"You are now friends with {username}!")
            except Friendship.DoesNotExist:
                messages.error(request, "Friend request not found.")
        else:
            Friendship.objects.create(
                from_user=from_profile,
                to_user=to_profile
            )
            messages.success(request, f"Friend request sent to {username}!")

    return redirect('profiles:profile', username=username)

@login_required
def respond_friend_request(request, request_id, action):
    if request.method == 'POST':
        friend_request = get_object_or_404(
            Friendship,
            id=request_id,
            to_user=request.user.userprofile
        )

        if action == 'accept':
            friend_request.accepted = True
            friend_request.save()
            messages.success(request, f"You are now friends with {friend_request.from_user.user.username}!")
        else:
            friend_request.delete()
            messages.info(request, "Friend request declined.")

    return redirect('profiles:friend_list')


@login_required
def remove_friend(request, username):
    if request.method == 'POST':
        friend_profile = get_object_or_404(UserProfile, user__username=username)
        current_profile = request.user.userprofile

        Friendship.objects.filter(
            Q(from_user=current_profile, to_user=friend_profile) |
            Q(from_user=friend_profile, to_user=current_profile)
        ).delete()

        messages.success(request, f"{username} has been removed from your friends.")

    return redirect('profiles:friend_list')


@login_required
def current_user_profile(request):
    return redirect('profiles:profile', username=request.user.username)


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.none()
    suggestions = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id).select_related('userprofile')

        if not users.exists():
            suggestions = User.objects.filter(
                username__istartswith=query[:3]
            ).exclude(id=request.user.id).select_related('userprofile')[:5]

    return render(request, 'profiles/search_users.html', {
        'users': users,
        'suggestions': suggestions,
        'query': query
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        username = user.username

        # Log out the user before deletion to prevent any session issues
        logout(request)

        # Delete the user account (this will trigger the pre_delete signal)
        user.delete()

        messages.success(request, f'Your account ({username}) has been permanently deleted.')
        return redirect('login')  # Redirect to Django's built-in login page

    # If not a POST request, redirect to settings
    return redirect('profiles:settings')

@login_required
def preferences(request):
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        background = request.POST.get('background', 'purple')
        profile.background = background
        profile.save()
        messages.success(request, 'Preferences saved successfully!')
        return redirect('profiles:preferences')

    return render(request, 'profiles/preferences.html', {
        'selected_background': profile.background
    })