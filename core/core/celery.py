import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure Celery to use Tehran time zone settings
app.conf.enable_utc = False
app.conf.timezone = "Asia/Tehran"

# Celery Beat Configuration
app.conf.beat_schedule = {
    "deactivate-old-users": {
        "task": "accounts.tasks.deactivate_old_users",
        "schedule": crontab(
            hour=0, minute=0, day_of_week="mon"
        ),  # runs weekly on monday midnight
    },
}
