# products/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Review
import random
import string
from datetime import datetime, timedelta


@shared_task
def generate_product_code(product_id):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    product = Product.objects.get(id=product_id)
    product.code = code
    product.save()
    return code

@shared_task
def delete_old_reviews():
    threshold_date = datetime.now() - timedelta(days=30)
    deleted_count = Review.objects.filter(created_at__lt=threshold_date).delete()
    return deleted_count


@shared_task
def notify_new_category(category_id):
    from .models import Category
    category = Category.objects.get(id=category_id)
    send_mail(
        subject=f'Новая категория создана: {category.name}',
        message=f'Категория "{category.name}" была создана.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],  # можно поменять на email модератора
        fail_silently=False
    )
