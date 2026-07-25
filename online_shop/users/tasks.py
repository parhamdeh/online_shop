from celery import shared_task

# local apps
from online_shop.sms_gateway.services.sms_services import SMSService


@shared_task
def send_sms(phone: str, code: int):
    data = {
        "phone":phone,
        "message": f"your verfication code is {code}"
    }
    SMSService().send_otp(data=data)
    