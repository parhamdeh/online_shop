# third party apps

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView



class SeeProductDetail(BasePermission):
    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        if request.user.is_staff:
            return True

        return bool(
            request.user.is_authenticated,
        )

    def has_object_permission(self, request, view, obj):
        ...