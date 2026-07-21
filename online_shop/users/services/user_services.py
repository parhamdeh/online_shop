# local apps
from online_shop.users.models import BaseUserModel, OtpCodeModel, ProfileModel, CartModel
from online_shop.users.services.code_services import create_otp_code_for_user

# django built in apps
from django.db import transaction


def create_user(*, data: dict) -> BaseUserModel:
    return BaseUserModel.objects.create_user(
        username=data.get("username"),
        phone=data.get("phone"),
        password=data.get("password"),
        is_active=False,
    )

def create_profile(*, user: BaseUserModel) -> ProfileModel:
    return ProfileModel.objects.create(user=user)

def create_cart(*, user: BaseUserModel) -> CartModel:
    return CartModel.objects.create(user=user, products=None)

@transaction.atomic
def register(*, data: dict):
    user = create_user(data=data)
    create_profile(user=user)
    create_cart(user=user)

    return user

@transaction.atomic
def create_user_and_otp(*, data: dict) -> OtpCodeModel:
    user = register(data=data)
    otp = create_otp_code_for_user(phone=data["phone"])
    return otp

