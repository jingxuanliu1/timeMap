# timeMap/timeMap/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timeMap.settings')

app = Celery('timeMap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule.update({
    'send-daily-recaps-every-night': {
        'task': 'notifications.tasks.send_daily_recaps',
        'schedule': crontab(hour=21, minute=0),  # every day at 9pm
        #'schedule': crontab(minute='*/1')  # every minute (to test code)

    },
})
