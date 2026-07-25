from rest_framework import serializers

from online_shop.products.models import ProductsModel


class ProductDetailOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = "__all__"