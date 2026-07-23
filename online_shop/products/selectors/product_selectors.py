

# django built in apps
from django.db.models import QuerySet

# local apps
from online_shop.products.models import ProductsModel


def get_products_list(*, filters=None) -> QuerySet[ProductsModel]:
    filters = filters or {}
    return ProductsModel.objects.all()


    