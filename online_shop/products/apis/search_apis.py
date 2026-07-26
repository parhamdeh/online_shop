# third party apps
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# local apps
from online_shop.products.selectors.elastic import search_for_product
from online_shop.products.documents import ProductDocument
from online_shop.products.models import ProductsModel
from online_shop.products.apis.products.products_serializer import (
    ProductListOutputModelSerializer,
)



@extend_schema(
    tags=["search"],
    summary="Search Products",
    description=(
        "Search products using Elasticsearch.\n\n"
        "The search is performed on the following fields:\n"
        "- Title\n"
        "- Price\n"
        "- Content\n\n"
        "Example:\n"
        "`/api/products/search/?q=iphone`"
    ),
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Search keyword.",
            examples=[
                OpenApiExample(
                    "iPhone",
                    value="iph",
                ),
                OpenApiExample(
                    "Samsung",
                    value="sam",
                ),
                OpenApiExample(
                    "Laptop",
                    value="lap",
                ),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=ProductListOutputModelSerializer(many=True),
            description="Products retrieved successfully.",
        ),
    },
)
class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductListOutputModelSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")

        search = ProductDocument.search()

        if query:
            search = search.query(
                "multi_match",
                query=query,
                fields=["title", "content"],
            )

        if query.isdigit():
            search = search.query(
                "bool",
                should=[
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"],
                        }
                    },
                    {
                        "term": {
                            "price": int(query),
                        }
                    },
                ],
            )

        ids = [hit.meta.id for hit in search]

        return search_for_product(ids=ids)


@extend_schema(
    tags=["search"],
    summary="Product Autocomplete",
    description="Returns product suggestions while typing.",
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Search text",
        )
    ],
    responses={
        200: OpenApiResponse(description="Suggestions returned successfully."),
    },
)
class ProductAutocompleteAPIView(APIView):

    def get(self, request):
        query = request.query_params.get("q", "")

        if not query:
            return Response([])

        search = ProductDocument.search()

        search = search.suggest(
            "products_suggest",
            query,
            completion={
                "field": "suggest",
                "skip_duplicates": True,
            },
        )

        result = search.execute()

        suggestions = []

        for option in result.suggest.products_suggest[0].options:
            suggestions.append(
                {
                    "id": option._source.id,
                    "title": option._source.title,
                }
            )

        return Response(suggestions)