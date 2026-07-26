from rest_framework.serializers import BaseSerializer
from rest_framework.generics import CreateAPIView

# local apps
from online_shop.payment_gateway.apis.serializers import PaymentCreateSerializer
from online_shop.payment_gateway.services import create_payment


class CreatePaymentAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def perform_create(self, serializer):
        serializer.instance = create_payment(
            user=self.request.user,
            data=serializer.validated_data,
        )
