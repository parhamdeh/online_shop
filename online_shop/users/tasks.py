from celery import shared_task

# local apps
from online_shop.users.services.sms_services import send_otp


@shared_task
def send_sms(phone: str, code: int):
    send_otp(phone=phone, code=code)
    