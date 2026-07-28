# third party apps
from rest_framework import serializers

# local apps 
from online_shop.products.models import LikeModel

class LikeInputSerializer(serializers.Serializer):
    pass

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = (
            "id",
            "user",
            "product",
            "created_at",
        )
        read_only_fields = (
            "id",
            "user",
            "product",
        )
