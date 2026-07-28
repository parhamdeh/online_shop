from django.db.models import F

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.selectors.product_selectors import get_product_by_id
from online_shop.users.selectors.cart_selectors import get_cart_items
from online_shop.common.types import DjangoModelType
from online_shop.users.models import CartItemModel, CartModel

def increase_quantity(*, item: CartItemModel, data: dict) -> DjangoModelType[CartItemModel]:
    item.quantity = F("quantity") + data["quantity"]
    item.save(update_fields=["quantity"])
    item.refresh_from_db(fields=["quantity"])
    return item

def update_items_in_cart(*, item: CartItemModel, data: dict) -> DjangoModelType[CartItemModel]:
    item.quantity = data["quantity"]
    item.save(update_fields=["quantity"])
    item.refresh_from_db(fields=["quantity"])
    return item

def add_item_to_cart(*, data: dict, cart: CartModel) -> DjangoModelType[CartItemModel]:
    product = get_product_by_id(product_id=data["product"]).get()
    data["product"] = product
    item = get_cart_items(cart=cart, data=data).first()
    if item:
       return increase_quantity(item=item, data=data)

    return CartItemModel.objects.create(
        cart=cart,
        product=product,
        quantity=data["quantity"],
    )

def change_quantity_in_cart(*, data: dict, cart: CartModel) -> DjangoModelType[CartItemModel]:
    item = get_cart_items(data=data, cart=cart).first()
    if not item:
        raise ApplicationError(message="item does not exist!")
    if item:
        return update_items_in_cart(item=item, data=data)

def delete_item_from_cart(*, item: CartItemModel) -> None:
    item.delete()
