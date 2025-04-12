from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tasks')  # Link to the user
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)  # Class location or any place
    latitude = models.FloatField(null=True, blank=True)  # Latitude coordinate
    longitude = models.FloatField(null=True, blank=True)  # Longitude coordinate
    start_time = models.DateTimeField()  # When the task starts
    end_time = models.DateTimeField()  # When the task should end
    completed = models.BooleanField(default=False)
    travel_time = models.DurationField(null=True, blank=True)  # How long it takes to travel there

    def __str__(self):
        return f"{self.title} - {self.start_time}"

    def get_travel_time(self):
        return self.travel_time if self.travel_time else "Not calculated"

    class Meta:
        ordering = ['start_time']
