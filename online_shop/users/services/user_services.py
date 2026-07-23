# local apps
from online_shop.common.types import DjangoModelType
from online_shop.users.models import BaseUserModel, ProfileModel, CartModel, UserWallet
from online_shop.users.services.code_services import create_otp_code_for_user

# django built in apps
from django.db import transaction



def get_user_or_404(*, user_id: int) -> DjangoModelType[BaseUserModel]:
    ...

def create_user(*, data: dict) -> DjangoModelType[BaseUserModel]:
    return BaseUserModel.objects.create_user(
        username=data.get("username"),
        phone=data.get("phone"),
        password=data.get("password"),
        is_active=False,
    )

def create_profile(*, user: BaseUserModel) -> DjangoModelType[ProfileModel]:
    return ProfileModel.objects.create(user=user)

def create_cart(*, user: BaseUserModel) -> DjangoModelType[CartModel]:
    return CartModel.objects.create(user=user)

def create_wallet(*, user: BaseUserModel) -> DjangoModelType[UserWallet]:
    return UserWallet.objects.create(user=user, balance=0)

@transaction.atomic
def register(*, data: dict):
    user = create_user(data=data)
    create_profile(user=user)
    create_wallet(user=user)
    create_cart(user=user)

    return user

@transaction.atomic
def create_user_and_otp(*, data: dict):
    user = register(data=data)
    otp = create_otp_code_for_user(phone=data["phone"])
    return otp

def activate_user(*, phone: str):
    
    user = (
        BaseUserModel.objects
        .select_for_update()
        .get(phone=phone)
    )

    if not user.is_active:
        user.is_active = True
        user.save(update_fields=["is_active"])

    return user