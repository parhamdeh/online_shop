# django built in apps 
from django.urls import path

# local apps
from online_shop.products.apis.search_apis import ProductAutocompleteAPIView, ProductSearchAPIView
from online_shop.products.apis.products.products_apis import PostListsAPIView
from online_shop.products.apis.products.id.product_id_apis import ProductRetrieveAPIView


urlpatterns = [
    path(route="products/", view=PostListsAPIView.as_view(), name="list_products"),
    path(route="search/", view=ProductSearchAPIView.as_view(), name="search_products"),
    path(route="search/autocomplete/", view=ProductAutocompleteAPIView.as_view(), name="product_autocomplete_search"),
    path(route="product/<int:product_id>/", view=ProductRetrieveAPIView.as_view(), name="product_detail")


    
]
