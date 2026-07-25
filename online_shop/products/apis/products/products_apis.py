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
    OpenApiParameter,
    OpenApiResponse,
)


# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.api.throttle import UserRequestThrottle
from online_shop.products.apis.products.products_serializer import ProductListOutputModelSerializer
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.product_selectors import get_products_list


logger = logging.getLogger(__name__)


# product detail + comment list + likes list
# category detail
# category list
# videos ...
# discount
# add -> like, comment
@extend_schema(
    tags=["Products"],
    summary="List Products",
    description=(
        "Returns a list of products.\n\n"
        "Supports filtering by category and price range."
    ),
    parameters=[
        OpenApiParameter(
            name="category",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Category ID.",
        ),
        OpenApiParameter(
            name="min_price",
            type=float,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Minimum product price.",
        ),
        OpenApiParameter(
            name="max_price",
            type=float,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Maximum product price.",
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=ProductListOutputModelSerializer(many=True),
            description="Products retrieved successfully.",
        ),
    },
)
class PostListsAPIView(ListAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (AllowAny,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = ProductListOutputModelSerializer

    def get_queryset(self):
        try:
            filters = {
                "category": self.request.query_params.get("category"),
                "min_price": self.request.query_params.get("min_price"),
                "max_price": self.request.query_params.get("max_price"),
            }

            products = get_products_list(filters=filters)

        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=f"database error: {ex}")

        return products