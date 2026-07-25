from django.urls import path, include

app_name = "api"
urlpatterns = [
    path('account/', include(('online_shop.users.urls', 'account'))),
    path('product/', include(('online_shop.products.urls', 'products'))),
]
