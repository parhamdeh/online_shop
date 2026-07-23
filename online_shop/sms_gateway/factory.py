from config.django import base

from online_shop.sms_gateway.providers.kavenegar import KavenegarProvider
# from online_shop.sms_gateway.providers.melipayamak import MeliPayamakProvider



def get_sms_provider():

    provider = base.SMS_PROVIDER

    if provider == "kavenegar":
        return KavenegarProvider()

    # if provider == "melipayamak":
    #     return MeliPayamakProvider()

    raise ValueError("Invalid sms provider")