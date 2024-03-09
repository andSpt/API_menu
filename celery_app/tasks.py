import smtplib

from celery_app.celery_config import celery
from celery_app import utils as celery_utils
from app.schemas import UserResponse


@celery.task
def send_confirmation_email(username: str, confirmation_token: str):

    with smtplib.SMTP(celery_utils.SMTP_HOST, celery_utils.SMTP_PORT) as server:
        server.starttls()
        server.login(user=celery_utils.SMTP_USER, password=celery_utils.SMTP_PASSWORD)
        server.send_message(
            celery_utils.generate_confirmation_email(
                username=username, confirmation_token=confirmation_token
            )
        )
