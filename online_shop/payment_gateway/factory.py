from online_shop.payment_gateway.gateways.zarinpal import ZarinPalGateway

class GatewayFactory:

    @staticmethod
    def get(name):

        if name == "zarinpal":
            return ZarinPalGateway()

        raise NotImplementedError