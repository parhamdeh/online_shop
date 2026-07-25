from online_shop.products.models import LikeModel


def get_like_by_id(*, like_id: int) -> LikeModel:
    return LikeModel.objects.filter(id=like_id)