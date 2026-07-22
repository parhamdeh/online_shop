# local apps
from online_shop.users.tasks import send_sms


# django built in apps
from django.core import cache

# third party apps
import random

def create_otp_code_for_user(*, phone: str) -> int:
    code = str(random.randint(100000, 999999))
    print(code)
    cache.set(
        f"otp:{phone}",
        {
            "code": "483921",
            "phone": phone,
            "attempts": 0,
        },
        timeout=400,
        )
    send_sms.delay(code=code, phone=phone)
    

    return code

def check_otp_and_update_user_is_active(*, data: dict, phone: str):
    from online_shop.users.services.user_services import activate_user
    otp_data = cache.get(f"otp:{phone}")

    if otp_data is None:
        raise Exception("OTP expired")

    code = otp_data["code"]
    
    if code != data["code"] :
        otp_data["attempts"] += 1
        raise Exception("OTP is wrong")
    
    if otp_data["attempts"] > 2:
        raise Exception("OTP expired")
    
    cache.delete(f"otp:{phone}")
    return activate_user(phone=phone)
    


    