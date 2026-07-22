from os import access

from rest_framework.generics import UpdateAPIView
import logging
from typing import Any
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
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.users.apis.user_serializers import RefreshTokenOutputSerializer, VerifyOtpSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.services.code_services import check_otp_and_update_user_is_active
from online_shop.users.services.user_services import create_user_and_otp


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Authentication"],
    summary="Verify OTP",
    description=(
        "Verifies the one-time password (OTP) sent to the user's phone number. "
        "If the verification succeeds, the user account is activated and "
        "a pair of JWT access and refresh tokens is returned."
    ),
    request=VerifyOtpSerializer,
    responses={
        200: OpenApiResponse(
            response=RefreshTokenOutputSerializer,
            description="OTP verified successfully.",
        ),
        400: OpenApiResponse(
            description="Invalid or expired OTP.",
        ),
        401: OpenApiResponse(
            description="Unauthorized.",
        ),
        429: OpenApiResponse(
            description="Too many requests. Please try again later.",
        ),
        500: OpenApiResponse(
            description="Internal server error.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Verify OTP",
            summary="Successful verification",
            description="Verify the OTP code received by SMS.",
            request_only=True,
            value={
                "code": "483921"
            },
        ),
        OpenApiExample(
            name="Success Response",
            response_only=True,
            value={
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                "username": "johndoe",
                "phone": "09123456789"
            },
        ),
    ],
)
class VerifyOtpAPIView(UpdateAPIView):
    serializer_class   =  RefreshTokenOutputSerializer
    permission_classes =  (AllowAny,)
    throttle_classes   =  (UserRequestThrottle,)
    renderer_classes   =  (CustomResponseRenderer,)   


    def perform_update(self, serializer: type[BaseSerializer]) -> ...:
        try:
            phone = self.request.session["phone"]
            user = check_otp_and_update_user_is_active(data=serializer.validated_data, phone=phone)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError()
        
        return user
    
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_update(serializer=serializer)
        token = RefreshToken.for_user(user=user)
        out_put_data = {
            "access_token" : str(token.access_token),
            "refresh_token" : str(token),
            "user" : user,
        }
        
        
        return Response(
            data=self.get_serializer(
                 instance=out_put_data
            ).data,
            status=status.HTTP_200_OK,
        )
    
    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)