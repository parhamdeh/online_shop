# third party apps
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

# django built in apps
from django.core.exceptions import ValidationError as DjangoValidationError

# local apps
from online_shop.core.exceptions import ApplicationError
from online_shop.users.apis.login_serializer import UserOutputSerializer
from online_shop.users.validators import LetterValidator, NumberValidator, SpecialCharValidator
from online_shop.users.models import BaseUserModel


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = PhoneNumberField(region="IR",)
    password = serializers.CharField()
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
    
    def validate_password(self, value):
        validators = [LetterValidator(), NumberValidator(), SpecialCharValidator()]
        errors = []
        for validator in validators:
            try:
                validator.validate(value)
            except DjangoValidationError as e:
                errors.extend(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return value
        

class VerifyOtpSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="IR",)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs: dict) -> dict:
        phone = attrs.get("phone")
        if phone and len(str(phone).replace("+98", "0")) > 11:
            raise serializers.ValidationError("phone number is not valid")
        
        attrs["phone"] = str(phone).replace("+98", "0")
        return attrs


class RefreshTokenOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserOutputSerializer()
