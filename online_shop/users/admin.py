# Django Built-in modules   
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator
from django.core.validators import EMPTY_VALUES


# Local Apps
from online_shop.users.models import BaseUserModel, CartItemModel, OrderItemModel, OtpModel, ProfileModel, OrderModel, CartModel, UserWallet

# Third Party Packages
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator
from unfold.contrib.filters.admin import TextFilter, FieldTextFilter




@admin.register(BaseUserModel)
class BaseUserAdmin(ModelAdmin, UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    paginator = InfinitePaginator
    show_full_result_count = False

    list_display = (
        "id",
        "phone",
        "username",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "phone",
    )

    ordering = (
        "id",
    )
    list_select_related = [] 
    
    # فیلدها
    fieldsets = (
        (_("اطلاعات شخصی"), {
            "fields": ("username", "phone",)
        }),
        (_("مجوزات"), {
            "fields": ("is_staff", "is_superuser", "is_active", "user_permissions"),
            "classes": ("collapse",),  
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
    
    @admin.display(description='', empty_value='_')
    def display_truncate_user(self, obj):
        return Truncator(obj.username).chars(50)

    
@admin.register(ProfileModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "user",
    )

    search_fields = (
        "user.username",
    )

    ordering = (
        "id",
    )
    
@admin.register(UserWallet)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "user",
        "balance",
    )

    search_fields = (
        "user.username",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (_("اطلاعات شخصی"), {
            "fields": ("user", "balance",)
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(OrderModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "user",
        "total_price",
        "discount",
        "status",
    )

    search_fields = (
        "user.username",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (_("اطلاعات شخصی"), {
            "fields": ("user", "total_price", "status", "discount")
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(OrderItemModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "order.id",
        "product.title",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (_("اطلاعات "), {
            "fields": ("order", "product", "quantity", "price")
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


@admin.register(CartModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "user",
    )

    search_fields = (
        "user.id",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (_("اطلاعات "), {
            "fields": ("user",)
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
    


@admin.register(CartItemModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
    )

    search_fields = (
        "cart.id",
        "product.title",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (_("اطلاعات "), {
            "fields": ("cart", "product", "quantity",)
        }),
        (_("تاریخ‌ها"), {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
    



@admin.register(OtpModel)
class BaseUserAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "id",
        "phone",
    )