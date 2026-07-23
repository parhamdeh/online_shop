from online_shop.sms_gateway.factory import get_sms_provider


class SMSService:

    def __init__(self):
        self.provider = get_sms_provider()

    def send_otp(self, *, phone, code):
        return self.provider.send_verify_code(
            phone=phone,
            code=code
        )

    def send_message(self, *, phone, message):
        return self.provider.send(
            phone=phone,
            message=message
        )

    