# tasks/models.py - Corrected version
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=False)
    travel_time = models.DurationField(null=True, blank=True)
    priority = models.IntegerField(default=1)  # Add this missing field
    due_date = models.DateTimeField(null=True, blank=True)  # Add this missing field

    def __str__(self):
        return f"{self.title} - {self.start_time}"

    def get_travel_time(self):
        return self.travel_time if self.travel_time else "Not calculated"

    class Meta:
        ordering = ['-priority', 'due_date']  # Single Meta class with existing fields