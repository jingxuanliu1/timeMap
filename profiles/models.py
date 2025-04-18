from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Q  # Added this import


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField(max_length=255, blank=True, default='')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    social_media = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_friends(self):
        """Returns all accepted friends"""
        return UserProfile.objects.filter(
            Q(friendship_received__from_user=self, friendship_received__accepted=True) |
            Q(friendship_sent__to_user=self, friendship_sent__accepted=True)
        ).distinct()

    def get_pending_requests_received(self):
        """Returns pending friend requests received"""
        return Friendship.objects.filter(
            to_user=self,
            accepted=False
        )

    def get_pending_requests_sent(self):
        """Returns pending friend requests sent"""
        return Friendship.objects.filter(
            from_user=self,
            accepted=False
        )

    def is_friends_with(self, other_profile):
        """Check if friends with another user"""
        return Friendship.objects.filter(
            (Q(from_user=self) & Q(to_user=other_profile) & Q(accepted=True)) |
            (Q(from_user=other_profile) & Q(to_user=self) & Q(accepted=True))
        ).exists()

    def get_friendship_status(self, other_profile):
        """Returns friendship status between users"""
        if self.is_friends_with(other_profile):
            return 'friends'

        if Friendship.objects.filter(from_user=self, to_user=other_profile).exists():
            return 'request_sent'

        if Friendship.objects.filter(from_user=other_profile, to_user=self).exists():
            return 'request_received'

        return None


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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only create profile if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(
            user=instance,
            defaults={'gmail': instance.email or ''}
        )
        if not created:
            # Update existing profile if needed
            profile.gmail = instance.email or ''
            profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()