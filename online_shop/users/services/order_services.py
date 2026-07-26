
import dis
import random

from online_shop.common.types import DjangoModelType
from online_shop.core.exceptions import ApplicationError
from online_shop.users.selectors.order_selectors import get_discount
from online_shop.users.selectors.cart_selectors import total_price
from online_shop.users.models import BaseUserModel, OrderModel, OrderStatus


def check_price_with_discount(*, price: int, discount_percent:int) -> int:
    if not (0 <= discount_percent <= 100):
        raise ApplicationError(message="discount cant be more than 100 and less than 0")
 
    if price < 0:
        raise ValueError("price cant be negative")
 
    discount_amount = price * discount_percent // 100
    final_price = price - discount_amount
 
    return final_price

def transfer_cart_itmes_to_order_items(*, cart):
    ...

def create_order(*, user: BaseUserModel, data: dict) -> DjangoModelType[OrderModel]:
    total = total_price(cart=user.user_cart)
    discount_code = data["discount_code"]
    if not discount_code:
        discount = None
    else:
        try:
            discount = get_discount(discount_code=discount_code).get()
        except Exception as ex:
            raise ApplicationError(message=ex)
        total = check_price_with_discount(price=total, discount_percent=discount.percent)
    transfer_cart_itmes_to_order_items()
    return OrderModel.objects.create(user=user,
                                    total_price=total,
                                    status=OrderStatus.PENDING_PAYMENT,
                                    discount=discount
                                    )