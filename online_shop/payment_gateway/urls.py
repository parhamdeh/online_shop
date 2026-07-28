from django.urls import path



from online_shop.payment_gateway.apis import (
    create_payment_apis,
    verify_payment_apis,
)

urlpatterns = [
    # ----------------------------------buy with gateway urls--------------------#
    path(
        "create/",
        create_payment_apis.CreatePaymentAPIView.as_view(),
        name="payment-create",
    ),
    path(
        "verify/",
        verify_payment_apis.PaymentVerifyAPIView.as_view(),
        name="payment-verify",
    ),
]