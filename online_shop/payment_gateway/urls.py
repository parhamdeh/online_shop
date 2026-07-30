from django.urls import path



from online_shop.payment_gateway.apis.order_payment import create_payment_apis
from online_shop.payment_gateway.apis.wallet_charge.wallet_crate_payment import CreateWalletPaymentAPIView
from online_shop.payment_gateway.apis import (
    verify_payment_apis,
)

urlpatterns = [
    # ----------------------------------buy with gateway urls--------------------#
    path(
        route="create/",
        view=create_payment_apis.CreatePaymentAPIView.as_view(),
        name="payment-create",
    ),
    path(
        route="verify/",
        view=verify_payment_apis.PaymentVerifyAPIView.as_view(),
        name="payment-verify",
    ),
    # -------------------------------charge wallet -------------------------------#
    path(
        route="charge/",
        view=CreateWalletPaymentAPIView.as_view(),
        name="charge-wallet"
    )
]