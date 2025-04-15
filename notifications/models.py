from django.db import models
from django.contrib.auth.models import User

class NotificationSetting(models.Model):
    NOTIFICATION_CHOICES = [
        (5, '5 minutes before'),
        (10, '10 minutes before'),
        (15, '15 minutes before'),
        (20, '20 minutes before'),
        (30, '30 minutes before'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_before = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Notification Setting"
