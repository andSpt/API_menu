from sys import modules

from celery import Celery
from app.config import settings

rabbitmq_url: str = settings.rabbitmq_url


if "pytest" in modules:
    rabbitmq_url: str = settings.test_rabbitmq

celery = Celery(__name__, broker=rabbitmq_url)
