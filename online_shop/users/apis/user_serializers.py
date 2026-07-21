# third party apps
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

# local apps
from online_shop.users.validators import LetterValidator, NumberValidator, SpecialCharValidator
from online_shop.users.models import BaseUserModel


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = PhoneNumberField(region="IR",)
    password = serializers.CharField(validators=[
        LetterValidator(),
        NumberValidator(),
        SpecialCharValidator(),
    ])
    confirm_password = serializers.CharField()


    def validate(self, attrs: dict) -> dict:
        phone = attrs.get("phone")
        if phone and len(str(phone).replace("+98", "0")) > 11:
            raise serializers.ValidationError("phone number is not valid")
        
        attrs["phone"] = str(phone).replace("+98", "0")
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("passwords must be match")
        attrs.pop("confirm_password")

        return attrs
    

class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class RefreshTokenOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    username = serializers.CharField()
    phone = phone = PhoneNumberField(
        region="IR",
    )
