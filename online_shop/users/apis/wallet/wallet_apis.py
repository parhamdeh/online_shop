# third party apps
import logging
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.users.permissions import IsALLowToSeeProfile
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.users.selectors.user_selectors import get_user_wallet
from online_shop.users.apis.id.users_id_serializer import WalletOutputSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.payment_gateway.services import use_wallet_for_buy_product


logger = logging.getLogger(__name__)



@extend_schema(
    tags=["Wallet"],
    summary="Get user wallet",
    description="Retrieve wallet information of a specific user.",
    responses={
        200: WalletOutputSerializer,
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Wallet not found"),
    },
)
class RetrieveWalletAPIView(RetrieveAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = WalletOutputSerializer
    renderer_classes = [CustomResponseRenderer]

    def get_object(self):
        try:
            wallet = get_user_wallet(user=self.request.user).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(f"database error {ex}")
        
        self.check_object_permissions(self.request, wallet)
        return wallet

@extend_schema(
    tags=["Wallet"],
    summary="Pay Order Using Wallet",
    description=(
        "Pay a pending order using the authenticated user's wallet balance.\n\n"
        "This endpoint:\n"
        "- Checks that the order belongs to the authenticated user.\n"
        "- Verifies the wallet has sufficient balance.\n"
        "- Deducts the order amount from the user's wallet.\n"
        "- Transfers the amount to the administrator wallet.\n"
        "- Marks the order as paid.\n"
        "- Creates the required payment and transaction records."
    ),
    request=None,
    responses={
        201: OpenApiResponse(
            response=WalletOutputSerializer,
            description="Order paid successfully using wallet balance.",
        ),
        400: OpenApiResponse(
            description="Insufficient wallet balance or invalid order.",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided.",
        ),
        403: OpenApiResponse(
            description="Permission denied.",
        ),
        404: OpenApiResponse(
            description="Order not found.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Successful Payment",
            value={
                "success": True,
                "message": "Order paid successfully using wallet.",
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Insufficient Balance",
            value={
                "success": False,
                "message": "Insufficient wallet balance.",
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)
class UseWalletForBuyProductAPIView(CreateAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = WalletOutputSerializer
    renderer_classes = [CustomResponseRenderer]

    def perform_create(self, serializer):
        serializer.instance = use_wallet_for_buy_product(
            order_id=self.kwargs["order_id"],
            user=self.request.user,
        )