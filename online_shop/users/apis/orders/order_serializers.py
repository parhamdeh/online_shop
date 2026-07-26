from rest_framework import serializers

from online_shop.users.models import OrderItemModel, OrderModel

class OrderItemsOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = "__all__"


class OrdersOutputSerializer(serializers.ModelSerializer):
    items = OrderItemsOutputSerializer( many=True,
    read_only=True,)

    class Meta:
        model = OrderModel
        fields = "__all__"

class OrdersInputSerializer(serializers.Serializer):
    discount_code = serializers.CharField(required=False,
    allow_blank=True,)
