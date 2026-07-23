# django buit in apps
from django.db import models
from django.utils.translation import gettext_lazy as _

# local apps
from online_shop.common.models import BaseModel
from online_shop.users.models import BaseUserModel


class DiscountModel(BaseModel):
    code = ...
    percent = ...
    start_day = ...
    end_day = ...

class CategoryModel(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("نام دسته بندی"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _( 'دسته بندی')
        verbose_name_plural = _('دسته بندی')

    def __str__(self):
        return self.name


class ProductsModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="product_category",  verbose_name=_("دسته بندی"))
    title = models.CharField(max_length=255, verbose_name=_("تیتر "), unique=True)
    content = models.TextField(verbose_name=_("محتوا"))
    image = models.ImageField(upload_to="products/images/",
        blank=True,
        null=True, verbose_name=_("عکس"))
    file = models.FileField(upload_to="products/files/")
    price = models.PositiveIntegerField(default=0, verbose_name=_("قیمت"))
    is_active = models.BooleanField(default=False, verbose_name=_("فعال"))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_("تعداد فروش"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("محصول ")
        verbose_name_plural = _("محصول ")
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["is_active", "-created_at"]),
            models.Index(fields=["-sales_count"]),
    ]
    
    def __str__(self):
        return self.title


class CommentsModel(BaseModel):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name="product_comment", verbose_name=_("محصول"))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_comment", verbose_name=_("محصول"))
    content = models.CharField(max_length=580)

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("کامنت ")
        verbose_name_plural = _("کامنت ")
        indexes = [
            models.Index(fields=["user", "product"]),
        ]
        
    def __str__(self):
        return self.user.username


class LikeModel(BaseModel):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name="product_liked", verbose_name=_("محصول"))
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_like", verbose_name=_("کاربر"))

    class Meta:
        ordering = ('-created_at',)
        verbose_name=_("لایک ")
        verbose_name_plural = _("لایک ")
        indexes = [
            models.Index(fields=["product", "user"]),
        ]
    
    def __str__(self):
        return self.user.username