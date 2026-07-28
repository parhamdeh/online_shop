# django built in apps 
from django.urls import path

# local apps
from online_shop.products.apis.category.id.category_id_apis import RetrieveCategoryAPIView
from online_shop.products.apis.search_apis import ProductAutocompleteAPIView, ProductSearchAPIView
from online_shop.products.apis.products.products_apis import PostListsAPIView
from online_shop.products.apis.products.id.product_id_apis import ProductRetrieveAPIView
from online_shop.products.apis.category.category_apis import CategoryListAPIView
from online_shop.products.apis.comments.comment_apis import AddCommentAPIView, DestroyCommentAPIView
from online_shop.products.apis.likes.like_apis import LikeAPIView, UnlikeAPIView


urlpatterns = [
    # ------------------------------products
    path(route="products/", view=PostListsAPIView.as_view(), name="list_products"),
    path(route="product/<int:product_id>/", view=ProductRetrieveAPIView.as_view(), name="product_detail"),
    # ----------------------------- searchs
    path(route="search/", view=ProductSearchAPIView.as_view(), name="search_products"),
    path(route="search/autocomplete/", view=ProductAutocompleteAPIView.as_view(), name="product_autocomplete_search"),
    # ------------------------------categories
    path(route="category/", view=CategoryListAPIView.as_view(), name="list_categories"),
    path(route="category/<int:category_id>/", view=RetrieveCategoryAPIView.as_view(), name="category_detail"),
    # ------------------------------comments
    path(route="comment/<int:product_id>/", view=AddCommentAPIView.as_view(), name="add_comments"),
    path(route="delete_comment/<int:comment_id>/", view=DestroyCommentAPIView.as_view(), name="delete_comment"),
    # ------------------------------likes
    path(route="like/<int:product_id>/", view=LikeAPIView.as_view(), name="like"),
    path(route="unlike/<int:like_id>/", view=UnlikeAPIView.as_view(), name="unlike"),

    
]
