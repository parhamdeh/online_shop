from online_shop.common.types import DjangoModelType
from online_shop.products.models import CategoryModel

from django.db.models import QuerySet


def get_categories_list() -> QuerySet[CategoryModel]:
    return CategoryModel.objects.all()

def get_category_by_id(*, category_id: int) -> DjangoModelType[CategoryModel]:
    return CategoryModel.objects.filter(id=category_id)