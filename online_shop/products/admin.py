# Django Built-in modules
import os

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import format_html

# Third Party Packages
from unfold.admin import ModelAdmin
from unfold.paginator import InfinitePaginator

# Local Apps
from online_shop.products.models import (
    DiscountModel,
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
        "category",
        "is_active",
        "sales_count",
        "image_preview",
        "file_preview",
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
        "category__name",
    )

    autocomplete_fields = (
        "category",
    )

    readonly_fields = (
        "created_at",
        "image_preview",
        "file_preview",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "category",
    )

    save_on_top = True
    list_per_page = 30

    fieldsets = (
        (_("اطلاعات اصلی"), {
            "fields": (
                "category",
                "is_active",
                "sales_count",
            )
        }),
        (_("محتوا"), {
            "fields": (
                "title",
                "content",
                ("image", "image_preview"),
                ("file", "file_preview"),
                "price",
            ),
            "classes": ("tab",),
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="خلاصه محتوا")
    def display_truncate_post(self, obj):
        return Truncator(obj.content).chars(50)

    @admin.display(description="تصویر")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:90px;height:70px;object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "-"

    @admin.display(description="فایل")
    def file_preview(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">📄 {}</a>',
                obj.file.url,
                os.path.basename(obj.file.name),
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
        (_("دسته‌بندی"), {
            "fields": (
                "name",
            ),
            "classes": ("tab",),
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="نام")
    def display_truncate_category(self, obj):
        return Truncator(obj.name).chars(50)


@admin.register(CommentsModel)
class CommentAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    readonly_fields = (
        "created_at",
    )

    list_display = (
        "id",
        "display_truncate_comment",
        "get_username",
        "product",
        "created_at",
    )

    search_fields = (
        "content",
        "user__username",
        "product__title",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "product",
    )

    fieldsets = (
        (_("اطلاعات"), {
            "fields": (
                "product",
                "user",
                "content",
            ),
            "classes": ("tab",),
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="کامنت")
    def display_truncate_comment(self, obj):
        return Truncator(obj.content).chars(50)

    @admin.display(description="کاربر")
    def get_username(self, obj):
        return obj.user.username


@admin.register(LikeModel)
class LikeAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    readonly_fields = (
        "created_at",
    )

    list_display = (
        "id",
        "get_username",
        "get_product",
        "created_at",
    )

    search_fields = (
        "user__username",
        "product__title",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "product",
    )

    fieldsets = (
        (_("اطلاعات"), {
            "fields": (
                "user",
                "product",
            ),
            "classes": ("tab",),
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="محصول")
    def get_product(self, obj):
        return obj.product.title

    @admin.display(description="کاربر")
    def get_username(self, obj):
        return obj.user.username


@admin.register(DiscountModel)
class DiscountAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    readonly_fields = (
        "created_at",
    )

    list_display = (
        "id",
        "code",
        "percent",
        "end_date",
    )

    search_fields = (
        "code",
        "percent",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
            (_("اطلاعات"), {
                "fields": (
                    "code",
                    "percent",
                ),
                "classes": ("tab",),
            }),
            (_("تاریخ‌ها"), {
                "fields": (
                    "end_date",
                ),
                "classes": ("collapse",),
            }),
        )
