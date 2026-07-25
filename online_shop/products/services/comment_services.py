from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.products.models import CommentsModel
from online_shop.products.selectors.product_selectors import get_product_by_id
from online_shop.products.selectors.comment_selectors import get_comment_by_id


def create_comment(*, data: dict, product_id: int, user) -> DjangoModelType[CommentsModel]:
    try:
        product = get_product_by_id(product_id=product_id).get()
    except Exception as ex:
        raise ApplicationError(message=ex)
    return CommentsModel.objects.create(
        content=data["content"],
        product=product,
        user=user
    )

def delete_comment(*, comment):
    comment.delete()