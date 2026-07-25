from online_shop.common.types import DjangoModelType
from online_shop.products.models import CommentsModel


def get_comment_by_id(*, comment_id: int) -> DjangoModelType[CommentsModel]:
    return CommentsModel.objects.filter(id=comment_id)