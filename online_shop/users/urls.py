# django built in apps
from django.urls import path, include

# third party apps


# local apps

from online_shop.users.apis.orders.order_apis import OrderRetrieveDestroyAPIView, OrdersListCreateAPIView
from online_shop.users.apis.cart.cart_apis import AddProductToCartAPIView, CartRetrieveUpdateAPIView, DeleteItemAPIView
from online_shop.users.apis.user_apis import UserRegisterAPIView
from online_shop.users.apis.id.user_id_apis import RetrieveProfileAPIView, UserChangeDetailsAPIView
from online_shop.users.apis.login_apis import CustomTokenObtainPairView, CustomRefreshTokenAPIView
from online_shop.users.apis.wallet.wallet_apis import RetrieveWalletAPIView, UseWalletForBuyProductAPIView
from online_shop.users.apis.user_verify_apis import VerifyOtpAPIView


app_name = "account"
urlpatterns = [
    #--------------------------------- authentication
    path(route="register/", view=UserRegisterAPIView.as_view(), name="register"),
    path(route="verify/", view=VerifyOtpAPIView.as_view(), name="verify-otp"),
     path("account/", include(([
        path("login/", CustomTokenObtainPairView.as_view(), name="login"),
        path("refresh/", CustomRefreshTokenAPIView.as_view(), name="refresh"),

    ])), name="jwt"),
    # ---------------------------------- User Detail
    path(route="profile/<int:user_id>/", view=RetrieveProfileAPIView.as_view(), name="profile"),
    path(route="change_password/<int:user_id>/", view=UserChangeDetailsAPIView.as_view(), name="change_password"),
    # path(route="order/<int:user_id>/", view=RetrieveOrdersAPIView.as_view(), name="order"),
    # -----------------------------------user cart
    path(route="add-item/", view=AddProductToCartAPIView.as_view(), name="add_to_cart"),
    path(route="delete-item/", view=DeleteItemAPIView.as_view(), name="delete_to_cart"),
    path(route="detail-cart/", view=CartRetrieveUpdateAPIView.as_view(), name="detail_cart"),
    # -------------------------------------orders
    path(route="crate_list_order/", view=OrdersListCreateAPIView.as_view(), name="list_crate_order"),
    path(route="order_detail/<int:order_id>/", view=OrderRetrieveDestroyAPIView.as_view(), name="order_detail"),
    # -------------------------------------wallet
    path(route="wallet/", view=RetrieveWalletAPIView.as_view(), name="wallet"),
    path(route="wallet/<int:order_id>/", view=UseWalletForBuyProductAPIView.as_view(), name="buy_with_wallet"),
]