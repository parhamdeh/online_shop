# third party apps
from rest_framework import serializers

# local apps
from online_shop.products.models import CategoryModel



class CategoryOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"
        