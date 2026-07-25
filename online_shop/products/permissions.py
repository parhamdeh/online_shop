# third party apps
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.products.selectors.product_selectors import user_bought_product



class SeeProductDetail(BasePermission):
    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        if request.user.is_staff:
            return True

        return bool(
            request.user.is_authenticated,
        )

    def has_object_permission(self, request, view, obj):
        return user_bought_product(
            user=request.user,
            product=obj,
        ).exists()


class DeleteCommentAndLike(BasePermission):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj) -> bool:
        return bool(
            request.user.is_authenticated and (
                obj.user == request.user
            )
        )