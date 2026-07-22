# Third Party Packages
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

# Local Apps
from .login_serializer import CustomTokenObtainPairSerializer

@extend_schema(
    tags=["Authentication"],)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Authentication"],)
class CustomRefreshTokenAPIView(TokenRefreshView):
    pass
    