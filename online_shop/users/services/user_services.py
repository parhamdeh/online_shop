# local apps
from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.users.selectors.user_selectors import get_user_by_id
from online_shop.users.models import BaseUserModel, ProfileModel, CartModel, UserWallet
from online_shop.users.services.code_services import create_otp_code_for_user
from online_shop.users.selectors.user_selectors import get_inactive_users

# django built in apps
from django.db import transaction



def get_user_or_404(*, user_id: int) -> DjangoModelType[BaseUserModel]:
    try:
        user = get_user_by_id(user_id=user_id).get()
    except Exception as ex:
        raise ApplicationError(message=ex)
    return user

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

def update_user(*, updated_data: dict, user: BaseUserModel) -> DjangoModelType[BaseUserModel]:
    for key, value in updated_data.items():
        setattr(user, key, value)
    user.save(update_fields=updated_data.keys())
    return user

def full_update(*, data: dict, user_id: int) -> DjangoModelType[BaseUserModel]:
    user = get_user_or_404(user_id=user_id)
    return update_user(user=user, updated_data=data)

def partial_update(*, data: dict, user_id: int) -> DjangoModelType[BaseUserModel]:
    user = get_user_or_404(user_id=user_id)
    return update_user(user=user, updated_data=data)

def delete_inactive_users():

    users = get_inactive_users()

    deleted_count, _ = users.delete()

    return deleted_count