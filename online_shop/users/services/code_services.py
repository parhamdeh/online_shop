# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.users.tasks import send_sms
from online_shop.users.models import OtpModel
from online_shop.common.types import DjangoModelType

# django built in apps
from django.core.cache import cache

# third party apps
import random

def create_otp_code_for_user(*, phone: str) -> str:
    code = str(random.randint(100000, 999999))
    print(code)
    OtpModel.objects.create(code=code, phone=phone)
    send_sms.delay(code=int(code), phone=phone)
    # cache.set(
    #     phone,
    #     {
    #         "code": code,
    #         "phone": phone,
    #         "attempts": 0,
    #     },
    #     timeout=400,
    #     )

    return code


def check_otp(*, phone: str) -> str:
    return OtpModel.objects.filter(phone=phone)

def check_otp_and_update_user_is_active(*, data: dict):
    from online_shop.users.services.user_services import activate_user
    phone = data.get("phone")
    otp = check_otp(phone=phone).get()
    
    # otp_data = cache.get(phone)

    if otp is None:
        raise ApplicationError(f"OTP expired {phone}")

    code = otp.code
    
    if code != data["code"]:
        # otp_data["attempts"] += 1
        # cache.set(phone, otp_data, timeout=400)
        raise ApplicationError("OTP is wrong")
    
    # if otp_data["attempts"] > 2:
    #     raise ApplicationError("OTP expired")
    
    # cache.delete(phone)
    return activate_user(phone=phone)
    


    