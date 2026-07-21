# django buit in apps
from django.db import models
from django.utils.translation import gettext_lazy as _

# local apps
from online_shop.online_shop.common.models import BaseModel




class CategoryModel(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("نام دسته بندی"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _( 'دسته بندی')
        verbose_name_plural = _('دسته بندی')

    def __str__(self):
        return self.name


class ProductsModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="product-category",  verbose_name=_("دسته بندی"))
    title = models.CharField(max_length=255, verbose_name=_("تیتر "), unique=True)
    content = models.CharField(verbose_name=_("محتوا"))
    image = models.ImageField(upload_to="products/images/",
        blank=True,
        null=True, verbose_name=_("عکس"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("قیمت"))
    is_active = models.BooleanField(default=False, verbose_name=_("فعال"))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_("تعداد فروش"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("محصول ")
        verbose_name_plural = _("محصول ")
    
    def __str__(self):
        return self.title

