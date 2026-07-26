# third party apps
import logging
from typing import Any
from django.conf.locale import fr
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.users.apis.user_serializers import RegisterInputSerializer
from online_shop.users.permissions import IsALLowToSeeProfile
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.users.selectors.user_selectors import get_user_order, get_user_profile, get_user_list, get_user_wallet
from online_shop.users.apis.id.users_id_serializer import OrderOutputSerializer, ProfileSerializer, UserOutput, WalletOutputSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.services.user_services import partial_update


logger = logging.getLogger(__name__)

@extend_schema(
    tags=["Users"],
    summary="Get user profile",
    description="Retrieve profile information of a specific user.",
    responses={
        200: ProfileSerializer,
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Profile not found"),
    },
)
class RetrieveProfileAPIView(RetrieveAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = ProfileSerializer
    renderer_classes = [CustomResponseRenderer]

    def get_object(self):
        try:
            profile = get_user_profile(user_id=self.kwargs["user_id"]).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(f"database error {ex}")
        
        self.check_object_permissions(self.request, profile)
        return profile


@extend_schema(
    tags=["Users"],
    summary="Update user information",
    description="""
    Update user information partially.

    Only the owner of the profile can update their information.
    """,
    request=RegisterInputSerializer,
    responses={
        200: OpenApiResponse(
            response=UserOutput,
            description="User updated successfully"
        ),
        400: OpenApiResponse(
            description="Validation Error"
        ),
        403: OpenApiResponse(
            description="Permission Denied"
        ),
        404: OpenApiResponse(
            description="User Not Found"
        ),
    },
    examples=[
        OpenApiExample(
            "Request Example",
            value={
                "username": "mamad",
                "phone": "+989123456789",
                "password": "StrongPassowrd123#",
                "confirm_password": "StrongPassowrd123#",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Response Example",
            value={
                "username": "mamad",
                "phone": "+989123456789",
            },
            response_only=True,
        )
    ]
)
class UserChangeDetailsAPIView(UpdateAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = RegisterInputSerializer
    renderer_classes = [CustomResponseRenderer]
    lookup_url_kwarg = "user_id"

    def perform_update(self, serializer: BaseSerializer):
        try:
            user_id = self.kwargs["user_id"]
            user = partial_update(data=serializer.validated_data, user_id=user_id)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=ex)

        return user

    def update(self, request: Request, *args: Any, **kwargs: Any):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.perform_update(serializer=serializer)
        return Response(
            data=UserOutput(instance=user).data,
            status=status.HTTP_200_OK
        )

    
@extend_schema(
    tags=["Users"],
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
            wallet = get_user_wallet(user_id=self.kwargs["user_id"]).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(f"database error {ex}")
        
        self.check_object_permissions(self.request, wallet)
        return wallet


@extend_schema(
    tags=["Users"],
    summary="Get user order",
    description="Retrieve a user's order.",
    responses={
        200: OrderOutputSerializer,
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Order not found"),
    },
)
class RetrieveOrdersAPIView(RetrieveAPIView):
    permission_classes = [IsALLowToSeeProfile]
    throttle_classes = [UserRequestThrottle]
    serializer_class = OrderOutputSerializer
    renderer_classes = [CustomResponseRenderer]

    def get_object(self):
        try:
            order = get_user_order(user_id=self.kwargs["user_id"]).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(f"database error {ex}")
        
        self.check_object_permissions(self.request, order)
        return order


