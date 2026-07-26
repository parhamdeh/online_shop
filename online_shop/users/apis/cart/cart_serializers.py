from rest_framework import serializers

from online_shop.users.models import CartModel, CartItemModel
from online_shop.users.selectors.cart_selectors import total_price
from online_shop.products.apis.products.products_serializer import ProductListOutputModelSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListOutputModelSerializer()

    class Meta:
        model = CartItemModel
        fields = (
            "id",
            "product",
            "quantity",
        )

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = (
            "id",
            "items",
            "total",
        )

    def get_total(self, obj):
        return total_price(cart=obj)