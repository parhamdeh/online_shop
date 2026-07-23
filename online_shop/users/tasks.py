from celery import shared_task

# local apps
from online_shop.sms_gateway.services.sms_services import SMSService


@shared_task
def send_sms(phone: str, code: int):
    SMSService().send_otp(phone=phone, code=code)
    