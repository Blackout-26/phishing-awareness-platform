import os
from celery import Celery

# Updated to match your split settings folder structure
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core')

# Read config from Django settings, using the 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically find background tasks in all your installed apps
app.autodiscover_tasks()