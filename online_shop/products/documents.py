from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from online_shop.products.models import ProductsModel


@registry.register_document
class ProductDocument(Document):
    suggest = fields.CompletionField()

    class Index:
        name = "products"

    class Django:
        model = ProductsModel

        fields = [
            "id",
            "title",
            "content",
            "price",
        ]

    def prepare_suggest(self, instance):
        return {
            "input": [
                instance.title,
            ]
        }