

from online_shop.core.exceptions import ApplicationError
from online_shop.users.models import BaseUserModel
from online_shop.products.models import LikeModel, ProductsModel
from online_shop.common.types import DjangoModelType
from online_shop.products.selectors.like_selectors import get_like_by_id


def create_like(*, user: BaseUserModel, product: ProductsModel) -> LikeModel:
    return LikeModel.objects.create(
        user=user,
        product=product,
    )

def delete_like(*, like_id: int) :
    try:
        like = get_like_by_id(like_id=like_id).get()
        like.delete()
    except Exception as ex:
        raise ApplicationError(message=str(ex))
