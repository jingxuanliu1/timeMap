# notifications/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from gmail_utils import send_notification_email

@shared_task
def send_upcoming_task_notifications():
    print("Checking for upcoming tasks...")
    now = timezone.now()
    for task in Task.objects.filter(
        completed=False,
        notify_before__isnull=False,
        start_time__range=(now + timedelta(minutes=0), now + timedelta(minutes=30))
    ):
        notify_time = task.start_time - timedelta(minutes=task.notify_before)
        if notify_time <= now:
            print(f"Sending email for task: {task.title}")
            send_notification_email(
                to=task.user.email,
                subject="Upcoming Task Reminder",
                body=f"Your task \"{task.title}\" is due at {task.start_time.strftime('%Y-%m-%d %H:%M')}!"
            )
