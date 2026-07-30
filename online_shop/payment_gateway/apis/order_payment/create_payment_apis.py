from rest_framework.serializers import BaseSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

# local apps
from online_shop.online_shop.payment_gateway.apis.order_payment.serializers import PaymentCreateOutputSerializer, PaymentCreateSerializer
from online_shop.payment_gateway.services import call_zarinpal


@extend_schema(
    tags=["Payment"],
    summary="Create a new payment request",
    description=(
        "Initiates a payment through the Zarinpal gateway. Supports two payment types: "
        "paying for an existing order (`order`) or charging the user's wallet (`wallet_charge`). "
        "Returns the payment gateway redirect URL for the client to follow."
    ),
    request=PaymentCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=PaymentCreateSerializer,
            description="Payment initiated successfully; redirect URL included.",
        ),
        400: OpenApiResponse(description="Invalid request data."),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
        500: OpenApiResponse(description="Payment gateway error."),
    },
    examples=[
        OpenApiExample(
            name="Pay for an order",
            request_only=True,
            value={"order_id": 42},
        ),
    ],
)

class CreatePaymentAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = call_zarinpal(
            user=request.user,
            data=serializer.validated_data,
        )

        output = PaymentCreateOutputSerializer(result)

        return Response(output.data, status=status.HTTP_201_CREATED)