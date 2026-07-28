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
        return obj.product_liked.count()

    def get_is_liked(self, obj):
        request = self.context["request"]

        if request.user.is_anonymous:
            return False

        return obj.product_liked.filter(user=request.user).exists()

    def get_comments(self, obj):
        comments = (
        obj.product_comment
        .select_related("user")
        .order_by("-created_at")[:5]
    )

        return CommentSerializer(
            comments,
            many=True,
            context=self.context
        ).data