from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
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
    profile = request.user.userprofile
    query = request.GET.get('q', '')
    search_results = None

    if query:
        search_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(userprofile__gmail__icontains=query)
        ).exclude(id=request.user.id).select_related('userprofile')

    # Convert UserProfile objects to User objects for the friends list
    friends_users = [friendship.user for friendship in profile.get_friends()]

    return render(request, 'profiles/friend_list.html', {
        'friends': friends_users,  # Now passing User objects instead of UserProfile
        'pending_requests': profile.get_pending_requests_received(),
        'sent_requests': profile.get_pending_requests_sent(),
        'search_results': search_results,
        'query': query
    })


@login_required
def send_friend_request(request, username):
    if request.method == 'POST':
        to_user = get_object_or_404(UserProfile, user__username=username)
        from_user = request.user.userprofile

        if from_user == to_user:
            messages.error(request, "You cannot send a friend request to yourself.")
        elif from_user.get_friendship_status(to_user) == 'request_sent':
            messages.warning(request, "Friend request already sent.")
        elif from_user.get_friendship_status(to_user) == 'request_received':
            # Accept existing request
            friendship = Friendship.objects.get(from_user=to_user, to_user=from_user)
            friendship.accepted = True
            friendship.save()
            messages.success(request, f"You are now friends with {username}!")
        elif from_user.get_friendship_status(to_user) == 'friends':
            messages.info(request, f"You are already friends with {username}.")
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

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(userprofile__gmail__icontains=query)
        ).exclude(id=request.user.id).select_related('userprofile')

    return render(request, 'profiles/search_users.html', {
        'users': users,
        'query': query
    })