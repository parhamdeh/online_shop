# third party apps
import logging
from typing import Any
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
from online_shop.users.permissions import IsALLowToSeeProfile
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.users.selectors.user_selectors import get_user_profile
from online_shop.users.apis.id.users_id_serializer import ProfileSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.users.services.code_services import create_otp_code_for_user
from online_shop.users.services.user_services import create_user_and_otp


logger = logging.getLogger(__name__)


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


       
