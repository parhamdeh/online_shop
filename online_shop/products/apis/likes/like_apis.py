# third party apps
import logging
from typing import Any
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.selectors.product_selectors import get_product_by_id
from online_shop.products.apis.likes.like_serializers import LikeSerializer
from online_shop.products.permissions import DeleteCommentAndLike, SeeProductDetail
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.selectors.like_selectors import get_like_by_id
from online_shop.products.services.like_services import create_like, delete_like

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Likes"],
    summary="Like a product",
    description="Adds a like from the authenticated user to the specified product.",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the product to like.",
            required=True,
        ),
    ],
    request=None,
    responses={
        201: OpenApiResponse(
            response=LikeSerializer,
            description="Product liked successfully.",
        ),
        403: OpenApiResponse(description="You do not have permission to like this product."),
        404: OpenApiResponse(description="Product not found."),
        409: OpenApiResponse(description="You have already liked this product."),
        429: OpenApiResponse(description="Too many requests. Please try again later."),
    },
)
class LikeAPIView(CreateAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (SeeProductDetail,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = LikeSerializer

    def perform_create(self, serializer: BaseSerializer):
        product_id = self.kwargs["product_id"]
        try:
            product = get_product_by_id(product_id=product_id).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))

        self.check_object_permissions(self.request, product)

        try:
            like = create_like(product=product, user=self.request.user)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))

        serializer.instance = like


@extend_schema(
    tags=["Likes"],
    summary="Unlike a product",
    description="Removes a like from the specified product for the authenticated user.",
    parameters=[
        OpenApiParameter(
            name="like_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the like to remove.",
            required=True,
        ),
    ],
    responses={
        204: OpenApiResponse(description="Like removed successfully."),
        403: OpenApiResponse(description="You do not have permission to remove this like."),
        404: OpenApiResponse(description="Like not found."),
        429: OpenApiResponse(description="Too many requests. Please try again later."),
    },
)
class UnlikeAPIView(DestroyAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (DeleteCommentAndLike,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = LikeSerializer

    def get_object(self):
        try:
            obj = get_like_by_id(
                like_id=self.kwargs["like_id"],
            ).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))

        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        delete_like(like_id=self.kwargs["like_id"])