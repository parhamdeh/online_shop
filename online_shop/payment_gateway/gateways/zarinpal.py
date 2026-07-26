from online_shop.payment_gateway.interface import BaseGateway
from online_shop.payment_gateway.exception import GatewayError

import requests

from django.conf import settings


class ZarinPalGateway(BaseGateway):

    def request(self, payment: dict):
        payload = {
            "merchant_id": settings.MERCHANT,
            "amount": payment.get("price"),
            "description": payment.get('description'),
            "callback_url": settings.CALLBACK_URL,
            "metadata": {
                "mobile": str(payment.get('phone')),
            },
    }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        response = requests.post(
            settings.ZP_API_REQUEST,
            json=payload,
            headers=headers,
            timeout=10,
        )

        result = response.json()

        data = result.get("data", {})

        if data.get("code") != 100:
            raise GatewayError(result)

        authority = data["authority"]

        return {
            "authority": authority,
            "payment_url": f"{settings.ZP_API_STARTPAY}{authority}",
        }

    def verify(self, payment):
        ...