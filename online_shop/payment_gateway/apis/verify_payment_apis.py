from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from online_shop.payment_gateway.services import verify_payment


@extend_schema(
    tags=["Payment"],
    summary="Verify payment callback from Zarinpal",
    description=(
        "This endpoint is called by the Zarinpal gateway itself as a redirect after the user "
        "completes (or cancels) payment on the bank's page — not directly by the client app. "
        "It verifies the transaction and updates the order/wallet accordingly."
    ),
    parameters=[
        OpenApiParameter(
            name="Authority",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The transaction authority code returned by Zarinpal.",
            required=True,
        ),
        OpenApiParameter(
            name="Status",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Payment status returned by Zarinpal ('OK' or 'NOK').",
            required=True,
        ),
    ],
    responses={
        200: OpenApiResponse(description="Payment verified and processed."),
        400: OpenApiResponse(description="Invalid or failed transaction."),
    },
)
class PaymentVerifyAPIView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request):

        authority = request.query_params.get("Authority")
        status = request.query_params.get("Status")

        result = verify_payment(
            authority=authority,
            status=status,
            user=request.user,
        )

        return Response(result)