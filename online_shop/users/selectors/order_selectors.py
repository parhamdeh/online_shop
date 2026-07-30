

from django.db.models import QuerySet

from online_shop.common.types import DjangoModelType
from online_shop.products.models import DiscountModel
from online_shop.users.models import BaseUserModel, OrderModel, OrderItemModel


def get_list_user_orders(*, user: BaseUserModel) -> QuerySet[OrderModel]:
    return OrderModel.objects.filter(user=user)

def get_discount(*, discount_code: str) -> DiscountModel:
    return DiscountModel.objects.filter(code=discount_code)

def get_order_by_id(*, order_id: int, user: BaseUserModel) -> OrderModel:
    return OrderModel.objects.filter(user=user, id=order_id)

def get_order_items(*, order: OrderModel) -> QuerySet[OrderItemModel] :
    return OrderItemModel.objects.filter(order=order)

