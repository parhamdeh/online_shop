
# Local Apps
from online_shop.sms_gateway.interfaces.sms_provider import BaseSMSProvider
from config.django import base

# Third Party Packages
from kavenegar import KavenegarAPI



class KavenegarProvider(BaseSMSProvider):

    api = KavenegarAPI(base.KAVENEGAR_API_KEY)

    def send(self, *, phone, message: str):
        params = {
                    "sender" : base.KAVENEGAR_SENDER,
                    "receptor": phone,
                    "message": message,
                }
        
        return self.api.sms_send(params)

    def send_verify_code(self, *, phone, code):
        
        params = {
            "sender" : base.KAVENEGAR_SENDER,
            "receptor": phone,
            "message": f"Your verification code is: {code}",
        }

        return self.api.sms_send(params)

    





    