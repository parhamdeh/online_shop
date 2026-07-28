from django.urls import path, include

app_name = "api"
urlpatterns = [
    # ----------------------------------users urls--------------------#
    path('account/', include(('online_shop.users.urls', 'account'))),
    # ----------------------------------products urls--------------------#
    path('product/', include(('online_shop.products.urls', 'products'))),
    # ----------------------------------payments urls--------------------#
    path('payments/', include(('online_shop.payment_gateway.urls', 'payment_gateway'))),
]
