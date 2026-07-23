# local apps
from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.users.models import BaseUserModel, ProfileModel


def get_user_by_id(*, user_id: int) -> DjangoModelType[BaseUserModel]:
    return BaseUserModel.objects.filter(id=user_id)

def get_user_profile(*, user_id: int) -> DjangoModelType[ProfileModel]:
    try:
        user = get_user_by_id(user_id=user_id).get()
    except BaseUserModel.DoesNotExist:
        raise ApplicationError("User Not Found!")
    
    return ProfileModel.objects.filter(user=user)
     
