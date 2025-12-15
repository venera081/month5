
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from datetime import datetime, timedelta
import random
import string


@shared_task
def save_random_code(user_id):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    user = CustomUser.objects.get(id=user_id)
    user.confirmation_code = code
    user.save()
    return code

@shared_task
def delete_inactive_users():
    threshold_date = datetime.now() - timedelta(days=7)
    deleted_count = CustomUser.objects.filter(is_active=False, date_joined__lt=threshold_date).delete()
    return deleted_count

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Добро пожаловать!',
        'Спасибо за регистрацию на нашем сайте!',
        settings.EMAIL_HOST_USER,
        ["email"],
        fail_silently=False,
    )
    return "Ok"
