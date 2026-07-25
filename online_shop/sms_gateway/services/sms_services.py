from online_shop.sms_gateway.factory import get_sms_provider


class SMSService:

    def __init__(self):
        self.provider = get_sms_provider()

    def send_otp(self, *, data: dict):
        return self.provider.send(
            data=data,
        )

    