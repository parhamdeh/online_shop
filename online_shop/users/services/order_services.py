

from django.db import transaction
from django.db.models import F, Sum

from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.users.services.cart_services import delete_item_from_cart
from online_shop.users.selectors.order_selectors import get_discount, get_order_by_id
from online_shop.users.selectors.cart_selectors import get_all_cart_items, get_cart_items, total_price
from online_shop.users.models import BaseUserModel, CartItemModel, CartModel, OrderItemModel, OrderModel, OrderStatus


def check_price_with_discount(*, price: int, discount_percent:int) -> int:
    if not (0 <= discount_percent <= 100):
        raise ApplicationError(message="discount cant be more than 100 and less than 0")
 
    if price < 0:
        raise ValueError("price cant be negative")
 
    discount_amount = price * discount_percent // 100
    final_price = price - discount_amount
 
    return final_price

def create_order_item(*, order: OrderModel, cart_items: list) -> OrderItemModel:
    order_items = [
        OrderItemModel(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        for item in cart_items
    ]

    OrderItemModel.objects.bulk_create(order_items)

def transfer_cart_itmes_to_order_items(*, cart: CartModel, order: OrderModel):
    cart_items = get_all_cart_items(cart=cart)

    order_items = create_order_item(
        order=order,
        cart_items=cart_items
    )

    cart_items.delete()

    return order_items

@transaction.atomic
def create_order(*, user: BaseUserModel, data: dict) -> DjangoModelType[OrderModel]:
    total = total_price(cart=user.user_cart.first())
    discount_code = data["discount_code"]
    if not discount_code:
        discount = None
    else:
        try:
            discount = get_discount(discount_code=discount_code).get()
        except Exception as ex:
            raise ApplicationError(message=ex)
        total = check_price_with_discount(price=total, discount_percent=discount.percent)
    
    order = OrderModel.objects.create(user=user,
                                    total_price=total,
                                    status=OrderStatus.PENDING_PAYMENT,
                                    discount=discount
                                    )
    transfer_cart_itmes_to_order_items(cart=user.user_cart.first(), order=order)
    return order

def delete_order(*, order_id: int, user: BaseUserModel) -> None:
    order = get_order_by_id(order_id=order_id, user=user)
    order.delete()

def update_order(*, order: OrderModel):
    ...