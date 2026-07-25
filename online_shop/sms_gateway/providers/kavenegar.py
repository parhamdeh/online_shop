
# Local Apps
from online_shop.sms_gateway.interfaces.sms_provider import BaseSMSProvider
from config.django import base

# Third Party Packages
from kavenegar import KavenegarAPI



class KavenegarProvider(BaseSMSProvider):

    api = KavenegarAPI(base.KAVENEGAR_API_KEY)

    def send(self, *, data: dict):
        params = {
                    "sender" : base.KAVENEGAR_SENDER,
                    "receptor": data["phone"],
                    "message": data["message"],
                }
        
        return self.api.sms_send(params)

    





    