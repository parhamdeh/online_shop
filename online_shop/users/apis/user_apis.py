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

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.users.apis.user_serializers import RegisterInputSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.services.code_services import create_otp_code_for_user
from online_shop.users.services.user_services import create_user_and_otp


logger = logging.getLogger(__name__)


class UserRegisterAPIView(CreateAPIView):
    serializer_class = RegisterInputSerializer
    renderer_classes = [CustomResponseRenderer]
    permission_classes = (AllowAny,)
    throttle_classes = [UserRequestThrottle]


    def perform_create(self, serializer: type[BaseSerializer]):
        try:
            otp = create_user_and_otp()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError()
        
        serializer.instance = otp

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)

        return Response(data=serializer(instance=serializer.instance).data,
                        status=status.HTTP_201_CREATED)





