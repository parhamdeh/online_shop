from online_shop.common.types import DjangoModelType
from online_shop.users.models import CartModel, BaseUserModel, CartItemModel
from online_shop.core.exceptions import ApplicationError
from online_shop.users.selectors.user_selectors import get_user_by_id

from django.db.models import F, QuerySet, Sum


def get_user_cart(*, user_id: int) -> DjangoModelType[CartModel]:
    try:
        user = get_user_by_id(user_id=user_id).get()
    except BaseUserModel.DoesNotExist:
        raise ApplicationError("User Not Found!")
    
    return CartModel.objects.filter(user=user)

def get_cart_items(*, cart: CartModel, data: dict) -> QuerySet[CartItemModel]:
    return CartItemModel.objects.filter(
        cart=cart,
        product=data["product"],
    )

def get_all_cart_items(*, cart: CartModel) -> QuerySet[CartItemModel]:
    return CartItemModel.objects.filter(
            cart=cart,
        )

def total_price(cart: CartModel):
    return (
        cart.items.aggregate(
            total=Sum(
                F("quantity") * F("product__price")
            )
        )["total"]
        or 0
    )

def get_itme_by_id(*, item_id: int) -> DjangoModelType[CartItemModel]:
    return CartItemModel.objects.filter(id=item_id)