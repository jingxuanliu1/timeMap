from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile, Friendship
from django.contrib.auth.models import User


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
    profile = user.userprofile
    is_own_profile = (request.user == user)

    friendship_status = None
    request_id = None
    is_friend = False

    if not is_own_profile:
        current_profile = request.user.userprofile

        # Check friendship status
        if current_profile.is_friends_with(profile):
            friendship_status = 'accepted'
            is_friend = True
        else:
            # Check for pending requests
            outgoing_request = Friendship.objects.filter(
                from_user=current_profile,
                to_user=profile
            ).first()

            incoming_request = Friendship.objects.filter(
                from_user=profile,
                to_user=current_profile
            ).first()

            if outgoing_request:
                friendship_status = 'pending'
            elif incoming_request:
                friendship_status = 'request_received'
                request_id = incoming_request.id

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
    profile = request.user.userprofile
    friends = profile.get_friends()
    pending_requests_received = profile.get_pending_requests_received()
    pending_requests_sent = profile.get_pending_requests_sent()

    return render(request, 'profiles/friend_list.html', {
        'friends': friends,
        'pending_requests': pending_requests_received,
        'sent_requests': pending_requests_sent
    })


@login_required
def send_friend_request(request, username):
    if request.method == 'POST':
        to_user = get_object_or_404(UserProfile, user__username=username)
        from_user = request.user.userprofile

        if from_user == to_user:
            messages.error(request, "You cannot send a friend request to yourself.")
        elif Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            messages.warning(request, "Friend request already sent.")
        elif Friendship.objects.filter(from_user=to_user, to_user=from_user).exists():
            # If they already sent you a request, accept it
            friendship = Friendship.objects.get(from_user=to_user, to_user=from_user)
            friendship.accepted = True
            friendship.save()
            messages.success(request, f"You are now friends with {username}!")
        else:
            Friendship.objects.create(from_user=from_user, to_user=to_user)
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

        # Delete friendship in both directions
        Friendship.objects.filter(
            from_user=current_profile,
            to_user=friend_profile
        ).delete()

        Friendship.objects.filter(
            from_user=friend_profile,
            to_user=current_profile
        ).delete()

        messages.success(request, f"{username} has been removed from your friends.")

    return redirect('profiles:friend_list')


@login_required
def current_user_profile(request):
    return redirect('profiles:profile', username=request.user.username)