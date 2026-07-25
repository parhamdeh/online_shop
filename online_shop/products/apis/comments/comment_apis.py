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
from online_shop.products.selectors.comment_selectors import get_comment_by_id
from online_shop.products.apis.comments.comment_serializer import CommentSerializer, CommentInputSerializer
from online_shop.products.permissions import DeleteCommentAndLike, SeeProductDetail
from online_shop.api.throttle import UserRequestThrottle
from online_shop.api.renderer import CustomResponseRenderer
from online_shop.products.services.comment_services import create_comment, delete_comment


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Comments"],
    summary="Add a comment to a product",
    description="Creates a new comment on the specified product for the authenticated user.",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the product to comment on.",
            required=True,
        ),
    ],
    request=CommentSerializer,
    responses={
        201: OpenApiResponse(
            response=CommentSerializer,
            description="Comment created successfully.",
        ),
        400: OpenApiResponse(description="Invalid request data."),
        403: OpenApiResponse(description="You do not have permission to comment on this product."),
        404: OpenApiResponse(description="Product not found."),
        429: OpenApiResponse(description="Too many requests. Please try again later."),
    },
    examples=[
        OpenApiExample(
            name="Add Comment Request",
            summary="Valid comment request",
            request_only=True,
            value={"content": "این محصول عالی بود، ممنون."},
        ),
    ],
)
class AddCommentAPIView(CreateAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (SeeProductDetail,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer: BaseSerializer):
        product_id = self.kwargs["product_id"]
        product = get_product_by_id(product_id=product_id).get()
        self.check_object_permissions(self.request, product)
        try:
            comment = create_comment(serializer.validated_data, product_id=product_id, user=self.request.user)
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))

        return comment

    def create(self, request: Request, *args, **kwargs):
        serializer = CommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer=serializer)


@extend_schema(
    tags=["Comments"],
    summary="Delete a comment",
    description="Deletes a specific comment. Only the comment's author or an authorized user can delete it.",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the product the comment belongs to.",
            required=True,
        ),
        OpenApiParameter(
            name="comment_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the comment to delete.",
            required=True,
        ),
    ],
    responses={
        204: OpenApiResponse(description="Comment deleted successfully."),
        403: OpenApiResponse(description="You do not have permission to delete this comment."),
        404: OpenApiResponse(description="Comment not found."),
        429: OpenApiResponse(description="Too many requests. Please try again later."),
    },
)
class DestroyCommentAPIView(DestroyAPIView):
    throttle_classes = (UserRequestThrottle,)
    permission_classes = (DeleteCommentAndLike,)
    renderer_classes = (CustomResponseRenderer,)
    serializer_class = CommentSerializer

    def get_object(self):
        try:
            obj = get_comment_by_id(
                comment_id=self.kwargs["comment_id"],
            ).get()
        except Exception as ex:
            logger.exception(f"database error {ex}")
            raise ApplicationError(message=str(ex))

        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        delete_comment(product=instance)