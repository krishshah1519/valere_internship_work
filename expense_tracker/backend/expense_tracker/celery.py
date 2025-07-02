import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')

app = Celery('expense_tracker')

# Load settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks.py from all apps
app.autodiscover_tasks()

# 👇 Add this line to use django-celery-beat's database scheduler
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
