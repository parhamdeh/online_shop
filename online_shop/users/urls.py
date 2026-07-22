# django built in apps
from django.urls import path, include

# third party apps


# local apps
from online_shop.users.apis.user_apis import UserRegisterAPIView
from online_shop.users.apis.login_apis import CustomTokenObtainPairView, CustomRefreshTokenAPIView
from online_shop.users.apis.user_verify_apis import VerifyOtpAPIView


app_name = "account"
urlpatterns = [
    path(route="register/", view=UserRegisterAPIView.as_view(), name="register"),
    path(route="verify/", view=VerifyOtpAPIView.as_view(), name="verify-otp"),
     path("account/", include(([
        path("login/", CustomTokenObtainPairView.as_view(), name="login"),
        path("refresh/", CustomRefreshTokenAPIView.as_view(), name="refresh"),

    ])), name="jwt"),

]