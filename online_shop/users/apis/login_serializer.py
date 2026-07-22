# Third Party Packages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# Local Apps
from online_shop.users.models import BaseUserModel



class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUserModel
        exclude = ("password",)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["phone"] = str(user.phone)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserOutputSerializer(self.user).data

        return data