# third party apps
from rest_framework import serializers
# local apps
from online_shop.products.models import CategoryModel
from online_shop.products.apis.products.products_serializer import ProductListOutputModelSerializer



class CategoryDetailModelSerializers(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = (
            "name",
            "id",
            "products",
        )

    def get_products(self, obj):
        products = (
            obj.products
                .select_related("product_category")
                .order_by("-created_at")[:5]
        )
        return ProductListOutputModelSerializer(products, many=True).data