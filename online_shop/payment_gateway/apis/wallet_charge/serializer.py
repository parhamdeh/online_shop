from rest_framework import serializers

from online_shop.payment_gateway.enums import PaymentType




class PaymentCreateSerializer(serializers.Serializer):

    amount = serializers.IntegerField(
        required=True,
    )

    def validate(self, attrs: dict) -> dict:

        attrs["payment_type"] = PaymentType.WALLET_CHARGE

        return attrs


class PaymentCreateOutputSerializer(serializers.Serializer):
    authority = serializers.CharField()
    payment_url = serializers.URLField()