# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import format_html

# Third Party Packages
from unfold.paginator import InfinitePaginator
from unfold.admin import ModelAdmin


# Local Apps
from online_shop.products.models import (
    ProductsModel,
    CategoryModel,
    CommentsModel,
    LikeModel,
)


@admin.register(ProductsModel)
class ProductAdmin(ModelAdmin):
   
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "title",
        "price",
        "file",
        "category",
        "is_active",
        "sales_count",
        "image_preview",
        "created_at",
    )
    

    list_filter = (
        "category",
        "price",
        "is_active",
    )

    search_fields = (
        "title",
        "content",
    )

    autocomplete_fields = (
        "category",
    )

    readonly_fields = (
        "created_at",
        "image_preview",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "category",
    )

    save_on_top = True


    list_per_page = 30
    fieldsets = (
        (_("اطلاعات اصلی "), {
            "fields": ( "category", "is_active", "sales_count")
        }),
        (_("محتوا"), {
            "fields": ("title", "content", "image", "price", "file"),
            "classes": ("tab",),  
        }),
    )

    @admin.display(description='', empty_value='_')
    def display_truncate_post(self, obj):
        return Truncator(obj.content).chars(50)
    
    @admin.display(
    description="ویژه",
    boolean=True,
)
    def premium_status(self, obj):
        return obj.is_premium
    
    @admin.display(description="تصویر")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:90px;height:70px;object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "-"
    

@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    readonly_fields = (
    "created_at",
    )
    
    list_display = (
        "id",
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-created_at",
    )
 
    fieldsets = (
        (_("محتوا"), {
            "fields": ("name",),
            "classes": ("tab",),  
        }),
    )

    @admin.display(description='', empty_value='_')
    def display_truncate_category(self, obj):
        return Truncator(obj.name).chars(50)


@admin.register(CommentsModel)
class CommentAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    
    list_display = (
        "id",
        "content",
        "get_username",
        "product",
        "created_at",
    )
    search_fields = (
        "product",
        "get_username",
    )
    readonly_fields = (
    "created_at",
)

    ordering = (
        "-created_at",
    )
    list_select_related = ["user", "product"] 
    
  
    fieldsets = (
        (_("محتوا"), {
            "fields": ("product", "content", "user"),
            "classes": ("tab",),  
        }),
    )

    @admin.display(description='', empty_value='_')
    def display_truncate_comment(self, obj):
        return Truncator(obj.content).chars(50)

    @admin.display(description="User")
    def get_username(self, obj):
        return obj.user.username


@admin.register(LikeModel)
class FavoritPostAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    list_display = (
        "id",
        "get_username",
        "get_product",
        "created_at",
    )
    search_fields = (
        "product",
        "user",
    )
    ordering = (
        "-created_at",
    )
    list_select_related = (
    "user", "post",
)
    readonly_fields = (
    "created_at",
)

    fieldsets = (
        (_("نام"), {
            "fields": ("user",)
        }),
        (_("محتوا"), {
            "fields": ("product", ),
            "classes": ("tab",),  
        }),
    )

    @admin.display(description='', empty_value='_')
    def display_truncate_favorite_post(self, obj):
        return Truncator(obj.post.title).chars(50)

    @admin.display(description="Product")
    def get_product(self, obj):
        return obj.product.title

    @admin.display(description="User")
    def get_username(self, obj):
        return obj.user.username