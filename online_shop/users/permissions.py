
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.generics import RetrieveAPIView


class IsALLowToSeeProfile(BasePermission):
    def has_permission(self, request: Request, view: RetrieveAPIView) -> bool:
        if request.user.is_staff:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
    
    def has_object_permission(self, request: Request, view: RetrieveAPIView, obj):
        return obj.user.id == request.user.id
            
        