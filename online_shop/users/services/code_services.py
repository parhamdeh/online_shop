# local apps
from online_shop.users.models import OtpCodeModel, BaseUserModel

# django built in apps
from django.core import cache

# third party apps
import random

def create_otp_code_for_user(*, phone: str) -> OtpCodeModel:
    code = str(random.randint(100000, 999999))
    print(code)
    cache.set(
        f"otp:{phone}",
        {
            "code": "483921",
            "phone": phone,
            "attempts": 0,
            "created_at": "...",
        },
        timeout=400,
        )
    return code
    