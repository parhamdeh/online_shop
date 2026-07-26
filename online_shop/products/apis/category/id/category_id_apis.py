# third party apps
import logging
from typing import Any
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.apis.category.id.category_id_serializers import CategoryDetailModelSerializers
from online_shop.products.apis.category.category_serializers import CategoryOutputModelSerializer
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.category_selectors import get_category_by_id


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Categories"],
    summary="Retrieve a single category",
    description=(
        "Returns the details of a single product category by its ID, "
        "including its nested/related fields as defined in the serializer."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the category to retrieve.",
            required=True,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=CategoryDetailModelSerializers,
            description="Category retrieved successfully.",
        ),
        404: OpenApiResponse(
            description="Category not found.",
        ),
        429: OpenApiResponse(
            description="Too many requests. Please try again later.",
        ),
        500: OpenApiResponse(
            description="Internal server error.",
        ),
    },
)
class RetrieveCategoryAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    throttle_classes = (UserRequestThrottle,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = CategoryDetailModelSerializers

    def get_object(self):
        try:
            category = get_category_by_id(category_id=self.kwargs["category_id"]).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))
        return category