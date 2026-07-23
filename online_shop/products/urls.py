# django built in apps 
from django.urls import path

# local apps
from online_shop.products.apis.products.products_apis import PostListsAPIView


urlpatterns = [
    path(route="products/", view=PostListsAPIView.as_view(), name="list_products"),
    
]
