# third party apps
import logging
from typing import Any
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)


# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.apis.category.category_serializers import CategoryOutputModelSerializer
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.category_selectors import get_categories_list


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Products - Categories"],
    summary="List Categories",
    description="""
لیست تمام دسته‌بندی‌های محصولات را برمی‌گرداند.

این API عمومی است و نیازی به احراز هویت ندارد.
""",
    parameters=[
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            description="شماره صفحه",
            required=False,
        ),
    ],
    responses={
        200: CategoryOutputModelSerializer(many=True),
        429: OpenApiResponse(description="Too Many Requests"),
    },
)
class CategoryListAPIView(ListAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (AllowAny,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = CategoryOutputModelSerializer

    def get_queryset(self):
        return get_categories_list()