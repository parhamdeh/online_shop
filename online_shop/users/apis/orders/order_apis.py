# third party apps
import logging
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.serializers import BaseSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.users.services.order_services import create_order, delete_order
from online_shop.users.permissions import IsALLowToSeeProfile
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.apis.orders.order_serializers import OrdersOutputSerializer, OrdersInputSerializer
from online_shop.core.exceptions import ApplicationError
from online_shop.users.selectors.order_selectors import get_list_user_orders, get_order_by_id
from online_shop.users.services.cart_services import add_item_to_cart, change_quantity_in_cart, delete_item_from_cart

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Orders"],
    summary="List/Create Orders",
    description=(
        "Retrieve all orders for the authenticated user or "
        "create a new order from the current shopping cart."
    ),
    responses={
        200: OrdersOutputSerializer(many=True),
        201: OrdersOutputSerializer,
    },
)
class OrdersListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRequestThrottle,)
    renderer_classes = (CustomResponseRenderer,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrdersInputSerializer

        return OrdersOutputSerializer

    def get_queryset(self):
        try:
            return get_list_user_orders(user=self.request.user)
        except Exception as ex:
            logger.exception(f"there is no order for you!{ex}")
            raise ApplicationError(message="there is no order for you!")
        
    
    def perform_create(self, serializer: BaseSerializer):
        serializer.instance = create_order(data=serializer.validated_data, user=self.request.user)

@extend_schema(
    tags=["Orders"],
    summary="Retrieve and destroy an Order",
    description="Retrieve a specific order belonging to the authenticated user.",
    responses={
        200: OrdersOutputSerializer,
        404: OpenApiResponse(description="Order not found"),
    },
)
class OrderRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRequestThrottle,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = OrdersOutputSerializer

    def get_object(self):
        try:
            order = get_order_by_id(
            order_id=self.kwargs["order_id"],
            user=self.request.user,
            ).get()
        except Exception as ex:
            logger.exception(f"order not found")
            raise ApplicationError(message=ex)
        return order

    def destroy(self, request, *args, **kwargs):
        delete_order(user=request.user, order_id=self.kwargs["order_id"])
