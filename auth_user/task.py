from celery import shared_task
from django.core.mail import send_mail

from auth_user.models import User


@shared_task
def send_email(subject, message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
    return 'Send email successfully'


# @shared_task
# def delete_not_verify_users(is_verify=False):
#     User.objects.filter(is_verify=is_verify).delete()
#     return 'User success deleted'


# delete_not_verify_users.delay()
