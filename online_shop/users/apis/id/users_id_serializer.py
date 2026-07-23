from rest_framework import serializers
from online_shop.users.models import BaseUserModel, UserOrder, CartModel, UserWallet



class UserOutput(serializers.ModelSerializer):
    class Meta:

        model = BaseUserModel
        exclude = ("password",)


class OrderOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrder
        fields = "__all__"


class CartOutput(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = "__all__"


class WalletOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        exclude = ("user",)


class ProfileSerializer(serializers.Serializer):
    user = UserOutput()
    
