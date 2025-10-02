import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create a Celery application instance
# 'backend' is the name of your Django app where Celery is defined
app = Celery('backend')

# Load task settings from the Django settings file, including CELERY_BROKER_URL.
# Namespace='CELERY' means all Celery settings must start with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task files (e.g., backend/tasks.py) in all installed apps
app.autodiscover_tasks()

# Example task for testing configuration (optional)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
