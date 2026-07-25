# local apps
from online_shop.products.models import ProductsModel



def search_for_product(*, ids):
    return ProductsModel.objects.filter(id__in=ids)