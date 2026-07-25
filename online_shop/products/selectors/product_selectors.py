

# django built in apps
from django.db.models import QuerySet

# local apps
from online_shop.users.models import UserOrder
from online_shop.products.models import ProductsModel


def get_product_by_id(*, product_id: int) -> ProductsModel:
    return ProductsModel.objects.filter(id=product_id)

def get_products_list(*, filters=None) -> QuerySet[ProductsModel]:
    filters = filters or {}

    queryset = ProductsModel.objects.all()

    if filters.get("category"):
        queryset = queryset.filter(category_id=filters["category"])

    if filters.get("min_price"):
        queryset = queryset.filter(price__gte=filters["min_price"])

    if filters.get("max_price"):
        queryset = queryset.filter(price__lte=filters["max_price"])

    return queryset

def user_bought_product(*, user, product):
    return UserOrder.objects.filter(user=user, product=product)


    