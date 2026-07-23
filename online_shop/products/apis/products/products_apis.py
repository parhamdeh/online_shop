# third party apps
import logging
from typing import Any
from rest_framework.generics import ListAPIView
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
from online_shop.products.apis.products.products_serializer import ProductListOutputModelSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.product_selectors import get_products_list


logger = logging.getLogger(__name__)


# filter -> price, category
# search -> elastic
# product detail + comment list + likes list
# category detail
# category list
# videos ...
# discount
# add -> like, comment
# product list 
class PostListsAPIView(ListAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (AllowAny)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = ProductListOutputModelSerializer

    def get_queryset(self):
        try:
            products = get_products_list()
        except Exception as ex:
            logger.exception(f"database error {ex}")

        return products