from config.env import env
from celery.schedules import crontab

# https://docs.celeryq.dev/en/stable/userguide/configuration.html

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = 'django-db'

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Asia/Tehran"

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERY_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3

CELERY_BEAT_SCHEDULE = {
    "delete-inactive-users": {
        "task": "users.delete_inactive_users",
        "schedule": crontab(hour=0, minute=0),
    },
}