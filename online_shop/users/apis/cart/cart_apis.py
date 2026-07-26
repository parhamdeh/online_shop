# third party apps
import logging
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.serializers import BaseSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.users.permissions import IsALLowToSeeProfile
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.apis.cart.cart_serializers import CartSerializer
from online_shop.core.exceptions import ApplicationError
from online_shop.users.selectors.cart_selectors import get_itme_by_id, get_user_cart
from online_shop.users.services.cart_services import add_item_to_cart, change_quantity_in_cart, delete_item_from_cart

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Cart"],
    summary="Add product to cart",
    description=(
        "Adds a product to the authenticated user's shopping cart. "
        "If the product already exists in the cart, its quantity is increased."
    ),
    responses={
        201: CartSerializer,
    },
)
class AddProductToCartAPIView(CreateAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = CartSerializer
    renderer_classes = [CustomResponseRenderer]
    
    def perform_create(self, serializer: BaseSerializer):
        try:
            items = add_item_to_cart(data=serializer.validated_data, cart=self.request.user.user_cart)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=ex)

        serializer.instance = items

@extend_schema(
    tags=["Cart"],)
class CartRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    '''
    this is a class for handle user cart 
    add product, delete and update number of products
    and also user can see the total price of cart 
    '''
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRequestThrottle]
    serializer_class = CartSerializer
    renderer_classes = [CustomResponseRenderer]

    @extend_schema(
    tags=["Cart"],
    summary="Retrieve shopping cart",
    description=(
        "Returns the authenticated user's shopping cart, "
        "including all cart items and the total price."
    ),
    )
    def get_object(self):
        return self.request.user.user_cart

    @extend_schema(
    tags=["Cart"],
    summary="Update cart item quantity",
    description="Updates the quantity of a specific cart item.",
)
    def perform_update(self, serializer: BaseSerializer):
        try:
            items = change_quantity_in_cart(data=serializer.validated_data, cart=self.request.user.user_cart)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=f"database error {ex}")
        serializer.instance = items


@extend_schema(
    tags=["Cart"],
    summary="Remove product from cart",
    description="Removes a product from the shopping cart.",
)
class DeleteItemAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRequestThrottle]
    serializer_class = CartSerializer
    renderer_classes = [CustomResponseRenderer]

    def get_object(self):
        item_id = self.kwargs["item_id"]
        try:
            item = get_itme_by_id(item_id=item_id).get()
        except Exception as ex:
            logger.exception(f"item does not exist")
            raise ApplicationError(message=ex)

    def perform_destroy(self, instance):
        delete_item_from_cart(item=instance)