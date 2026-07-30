from rest_framework import serializers

from online_shop.payment_gateway.enums import PaymentType




class PaymentCreateSerializer(serializers.Serializer):

    order_id = serializers.IntegerField(
        required=True,
    )

    def validate(self, attrs):

        attrs["payment_type"] = PaymentType.ORDER

        return attrs


class PaymentCreateOutputSerializer(serializers.Serializer):
    authority = serializers.CharField()
    payment_url = serializers.URLField()