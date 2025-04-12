from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail = models.EmailField(unique=True, help_text="Please use a Gmail address.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Your phone number (e.g., +1234567890).")
    social_media = models.CharField(max_length=100, blank=True, null=True, help_text="Your social media handle (e.g., @username).")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, help_text="Upload your profile picture.")
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="A short introduction about yourself (max 500 characters).")

    def __str__(self):
        return f"{self.user.username}'s profile"
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, gmail=instance.email or '')