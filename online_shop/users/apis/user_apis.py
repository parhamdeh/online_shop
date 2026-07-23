# third party apps
import logging
from typing import Any
from rest_framework.generics import CreateAPIView
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
from online_shop.users.apis.user_serializers import RegisterInputSerializer, VerifyOtpSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.services.code_services import create_otp_code_for_user
from online_shop.users.services.user_services import create_user_and_otp


logger = logging.getLogger(__name__)



@extend_schema(
    tags=["Authentication"],
    summary="Register a new user",
    description=(
        "Creates a new inactive user account, generates a one-time password (OTP), "
        "and sends the verification code to the user's phone number. "
        "The account must be verified before login."
    ),
    request=RegisterInputSerializer,
    responses={
        201: OpenApiResponse(
            response=RegisterInputSerializer,
            description="User registered successfully. OTP has been sent.",
        ),
        400: OpenApiResponse(
            description="Invalid request data.",
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
            name="Register Request",
            summary="Valid registration request",
            description="Example request body for registering a new user.",
            request_only=True,
            value={
                "username": "johndoe",
                "phone": "09123456789",
                "password": "StrongPassword123!"
            },
        ),
    ],
)
class UserRegisterAPIView(CreateAPIView):
    serializer_class = RegisterInputSerializer
    renderer_classes = [CustomResponseRenderer]
    permission_classes = (AllowAny,)
    throttle_classes = [UserRequestThrottle]


    def perform_create(self, serializer: type[BaseSerializer]):
        try:
            otp = create_user_and_otp(data=serializer.validated_data)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(f"database error {ex}")
        
        logger.info(f" otp successfuly sent for user, otp.code :{otp}")
        return otp

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        
        return Response(data={"message : code sent you successfuly"},
                        status=status.HTTP_201_CREATED)





