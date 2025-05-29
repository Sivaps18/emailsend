from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import random
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_otp_email(email):
    otp = random.randint(100000, 999999)
    subject = 'Your OTP Code'
    message = f"<h1 style='color: red'>Your OTP code</h1>: {otp}"
    from_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f"Sent OTP {otp} to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")
        raise e

    return f"Sent OTP {otp} to {email}"
