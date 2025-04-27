from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tasks')  # Link to the user
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_location = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)  # Class location or any place
    latitude = models.FloatField(null=True, blank=True)  # Latitude coordinate
    longitude = models.FloatField(null=True, blank=True)  # Longitude coordinate
    latitude2 = models.FloatField(null=True, blank=True)  # Latitude coordinate
    longitude2 = models.FloatField(null=True, blank=True)  # Longitude coordinate
    start_time = models.DateTimeField()  # When the task starts
    end_time = models.DateTimeField()  # When the task should end
    completed = models.BooleanField(default=False)
    travel_time = models.DurationField(null=True, blank=True)  # How long it takes to travel there
    due_date = models.DateTimeField(null=True, blank=True)

    notify_before = models.IntegerField(
        choices=[
            (5, "5 minutes before"),
            (10, "10 minutes before"),
            (15, "15 minutes before"),
            (20, "20 minutes before"),
            (30, "30 minutes before"),
        ],
        null=True,
        blank=True,
        help_text="Send notification this many minutes before start"
    )

    notified = models.BooleanField(default=False)

    RECUR_CHOICES = [
        ('none', 'Do not repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    recur = models.CharField(max_length=10, choices=RECUR_CHOICES, default='none')

    def __str__(self):
        return f"{self.title} - {self.start_time}"

    def get_travel_time(self):
        return self.travel_time if self.travel_time else "Not calculated"

    class Meta:
        ordering = ['start_time']

# class for generating quotes using API
class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    fetched_date = models.DateField()
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quote} - {self.author}"

    class Meta:
        # Ensure only one quote per day
        unique_together = ['fetched_date']