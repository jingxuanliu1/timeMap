from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField(unique=True, help_text="Please use a Gmail address.")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    social_media = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_friends(self):
        """Returns all accepted friends"""
        # Friends where you accepted their request
        friends1 = UserProfile.objects.filter(
            friendship_received__from_user=self,
            friendship_received__accepted=True
        )
        # Friends where they accepted your request
        friends2 = UserProfile.objects.filter(
            friendship_sent__to_user=self,
            friendship_sent__accepted=True
        )
        return friends1.union(friends2).distinct()

    def get_pending_requests_received(self):
        """Returns pending friend requests you've received"""
        return Friendship.objects.filter(
            to_user=self,
            accepted=False
        )

    def get_pending_requests_sent(self):
        """Returns pending friend requests you've sent"""
        return Friendship.objects.filter(
            from_user=self,
            accepted=False
        )

    def is_friends_with(self, other_profile):
        """Check if this user is friends with another profile"""
        return (Friendship.objects.filter(
            from_user=self,
            to_user=other_profile,
            accepted=True
        ).exists() or Friendship.objects.filter(
            from_user=other_profile,
            to_user=self,
            accepted=True
        ).exists())

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
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, gmail=instance.email or '')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()