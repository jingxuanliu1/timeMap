from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField(unique=True, help_text="Please use a Gmail address.")
    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                    help_text="Your phone number (e.g., +1234567890).")
    social_media = models.CharField(max_length=100, blank=True, null=True,
                                    help_text="Your social media handle (e.g., @username).")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,
                                      help_text="Upload your profile picture.")
    bio = models.TextField(max_length=500, blank=True, null=True,
                           help_text="A short introduction about yourself (max 500 characters).")
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False,
                                     related_name='related_friends', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_friends(self):
        """Returns accepted friends"""
        return self.friends.filter(friendship_received__accepted=True)

    def get_pending_requests(self):
        """Returns pending friend requests"""
        return Friendship.objects.filter(to_user=self, accepted=False)


class Friendship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='friendship_sent',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='friendship_received',
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({'Accepted' if self.accepted else 'Pending'})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, gmail=instance.email or '')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()