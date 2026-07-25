# third party apps
from rest_framework import serializers

# local apps 
from online_shop.products.models import CommentsModel



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsModel
        fields = (
            "id",
            "user",
            "content",
            "created_at",
        )

class CommentInputSerializer(serializers.Serializer):
    content = serializers.CharField()