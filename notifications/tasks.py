# notifications/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from gmail_utils import send_gmail  # Gmail API
from django.template.loader import render_to_string

@shared_task
def send_upcoming_task_notifications():
    print("Checking for upcoming tasks...") # terminal debugging message
    now = timezone.now()
    upcoming_tasks = Task.objects.filter(
        completed=False,
        notified=False,  # ✅ prevent repetition
        notify_before__isnull=False,
        start_time__range=(now, now + timedelta(minutes=30))
    )

    for task in upcoming_tasks:
        notify_time = task.start_time - timedelta(minutes=task.notify_before)
        if notify_time <= now and not task.notified:
            print(f"📬 Sending Gmail for task: {task.title}")

            plain_text = f"Reminder: Your task '{task.title}' is scheduled at {task.start_time.strftime('%Y-%m-%d %H:%M')}."
            html_content = render_to_string("notifications/email_notification.html", {
                "task": task,
                "user": task.user,
            })

            send_gmail(
                to_email=task.user.email,
                subject=f"[TimeMap] Reminder: {task.title}",
                body=plain_text,
                html_body=html_content
            )

            task.notified = True
            task.save()
