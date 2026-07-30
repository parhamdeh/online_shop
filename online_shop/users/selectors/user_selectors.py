# django built in apps
from django.db.models import QuerySet
from django.utils import timezone


# local apps
from datetime import timedelta
from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.users.models import BaseUserModel, ProfileModel, UserWallet

def get_user_list() -> QuerySet[BaseUserModel]:
    return BaseUserModel.objects.all()

def get_user_by_id(*, user_id: int) -> DjangoModelType[BaseUserModel]:
    return BaseUserModel.objects.filter(id=user_id)


def get_user_wallet(*, user: BaseUserModel) -> DjangoModelType[UserWallet]:
    return UserWallet.objects.filter(user=user)

def get_admin_wallet():
    return UserWallet.objects.select_for_update().get(
        user__is_superuser=True,
    )

def get_user_profile(*, user_id: int) -> DjangoModelType[ProfileModel]:
    try:
        user = get_user_by_id(user_id=user_id).get()
    except BaseUserModel.DoesNotExist:
        raise ApplicationError("User Not Found!")
    
    return ProfileModel.objects.filter(user=user)

def get_inactive_users():
    return BaseUserModel.objects.filter(
        is_active=False,
        date_joined__lte=timezone.now() - timedelta(days=1),
    )

