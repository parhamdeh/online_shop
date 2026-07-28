from online_shop.payment_gateway.interface import BaseGateway
from online_shop.core.exceptions import ApplicationError
from online_shop.payment_gateway.exception import GatewayError

import requests

from config.django import local


class ZarinPalGateway(BaseGateway):

    def request(self, payment: dict):
        payload = {
            "merchant_id": local.MERCHANT,
            "amount": payment.get("price"),
            "description": payment.get('description'),
            "callback_url": local.CALLBACK_URL,
            "metadata": {
                "mobile": str(payment.get('phone')),
            },
    }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        response = requests.post(
            local.ZP_API_REQUEST,
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
            "payment_url": f"{local.ZP_API_STARTPAY}{authority}",
        }

    def verify(self, payment):
        payload = {
            "merchant_id": local.MERCHANT,
            "authority": payment.authority,
            "amount": int(payment.amount),
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        try:
            response = requests.post(
                local.ZP_API_VERIFY,
                json=payload,
                headers=headers,
                timeout=10,
            )
            result = response.json()

        except requests.RequestException:
            raise ApplicationError("Gateway unavailable.")

        data = result.get("data", {})
        

        if data.get("code") not in (100, 101):
            raise ApplicationError(
                result.get("errors") or
                data.get("message") or
                "ZarinPal verify failed."
            )

        
    
        return {
            "ref_id": data["ref_id"],
        }