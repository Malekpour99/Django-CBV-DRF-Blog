from datetime import timedelta
from celery import shared_task

from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def deactivate_old_users():
    three_months_ago = timezone.now() - timedelta(days=90)
    users_to_deactivate = User.objects.filter(
        last_login__lt=three_months_ago, is_active=True
    )

    for user in users_to_deactivate:
        user.is_active = False
        user.save()
