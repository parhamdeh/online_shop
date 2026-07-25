# third party apps
import logging
from typing import Any
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)


# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.permissions import SeeProductDetail
from online_shop.products.apis.products.id.product_id_serializers import ProductDetailOutputModelSerializer
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.product_selectors import get_product_by_id


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Products"],
    summary="Retrieve Product Details",
    description=(
        "Returns the details of a single product.\n\n"
        "Only authenticated users who have purchased the product "
        "or staff users can access this endpoint."
    ),
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="Product ID.",
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=ProductDetailOutputModelSerializer,
            description="Product retrieved successfully.",
        ),
        403: OpenApiResponse(
            description="You do not have permission to view this product.",
        ),
        404: OpenApiResponse(
            description="Product not found.",
        ),
    },
)
class ProductRetrieveAPIView(RetrieveAPIView):
    permission_classes = (SeeProductDetail,)
    throttle_classes = (UserRequestThrottle,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = ProductDetailOutputModelSerializer

    def get_object(self):
        try:
            product_id = self.kwargs["product_id"]
            product = get_product_by_id(product_id=product_id).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=ex)

        
        self.check_object_permissions(self.request, product)
        return product


