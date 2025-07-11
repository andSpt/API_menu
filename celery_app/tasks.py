import smtplib
from sys import modules

from celery import Celery

from app.config import settings
from celery_app import utils as celery_utils

rabbitmq_url: str = settings.rabbitmq_url


if "pytest" in modules:
    rabbitmq_url: str = settings.test_rabbitmq

celery = Celery(__name__, broker=rabbitmq_url)


@celery.task
def send_confirmation_email(username: str, confirmation_token: str, user_email: str):
    email = celery_utils.generate_confirmation_email(
        username=username, confirmation_token=confirmation_token, user_email=user_email
    )
    with smtplib.SMTP_SSL(celery_utils.SMTP_HOST, celery_utils.SMTP_PORT) as server:
        server.login(user=celery_utils.SMTP_USER, password=celery_utils.SMTP_PASSWORD)
        server.send_message(email)
