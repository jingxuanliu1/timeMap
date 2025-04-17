from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Q


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    social_media = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def get_friends(self):
        """Returns all accepted friends as UserProfile objects"""
        # Get friendships where this user is the sender and they're accepted
        sent_friendships = Friendship.objects.filter(
            from_user=self,
            accepted=True
        ).select_related('to_user__user')

        # Get friendships where this user is the receiver and they're accepted
        received_friendships = Friendship.objects.filter(
            to_user=self,
            accepted=True
        ).select_related('from_user__user')

        # Combine both lists and extract the friend profiles
        friends = []
        for friendship in sent_friendships:
            friends.append(friendship.to_user)
        for friendship in received_friendships:
            friends.append(friendship.from_user)

        return friends
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()

    def __str__(self):
        return f"{self.user.username}'s profile"

    # ... (keep all your existing methods) ...


class Friendship(models.Model):
    from_user = models.ForeignKey(
        UserProfile,
        related_name='friendship_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        UserProfile,
        related_name='friendship_received',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)


@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete user profile
    if hasattr(instance, 'userprofile'):
        instance.userprofile.delete()

    # Delete friendships where user is either sender or receiver
    Friendship.objects.filter(
        Q(from_user__user=instance) |
        Q(to_user__user=instance)
    ).delete()