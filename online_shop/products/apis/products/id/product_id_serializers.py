# third party apps
from rest_framework import serializers

# local apps
from online_shop.products.apis.comments.comment_serializer import CommentSerializer
from online_shop.products.models import ProductsModel


class ProductDetailOutputModelSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = ProductsModel
        fields = (
            "id",
            "title",
            "price",
            "content",
            "file",
            "likes_count",
            "is_liked",
            "comments",
        )


    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context["request"]

        if request.user.is_anonymous:
            return False

        return obj.likes.filter(user=request.user).exists()

    def get_comments(self, obj):
        comments = (
            obj.comments
            .select_related("user_comment")
            .order_by("-created_at")[:5]
        )

        return CommentSerializer(comments, many=True).data