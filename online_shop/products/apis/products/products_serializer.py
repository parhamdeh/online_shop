# third party apps
from rest_framework import serializers

# local apps
from online_shop.products.models import ProductsModel


class ProductListOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        exclude = ("video", "file", "content", "sales_count")