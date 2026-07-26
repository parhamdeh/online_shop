from rest_framework import serializers

from online_shop.payment_gateway.enums import PaymentType


class PaymentCreateSerializer(serializers.Serializer):
    payment_type = serializers.ChoiceField(
        choices=PaymentType.choices,
    )

    cart_id = serializers.IntegerField(
        required=False,
    )

    amount = serializers.IntegerField(
        required=False,
        min_value=1000,
    )

    def validate(self, attrs):

        payment_type = attrs["payment_type"]

        if payment_type == PaymentType.ORDER:

            if "cart_id" not in attrs:
                raise serializers.ValidationError(
                    {
                        "cart_id": "This field is required."
                    }
                )

        elif payment_type == PaymentType.WALLET_CHARGE:

            if "amount" not in attrs:
                raise serializers.ValidationError(
                    {
                        "amount": "This field is required."
                    }
                )

        return attrs