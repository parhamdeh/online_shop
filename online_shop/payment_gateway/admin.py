# Django Built-in modules
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from unfold.admin import ModelAdmin
from unfold.paginator import InfinitePaginator

# Local Apps
from online_shop.payment_gateway.models import PaymentModel


@admin.register(PaymentModel)
class PaymentAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    list_display = (
        "id",
        "user",
        "amount",
        "payment_type",
        "status",
        "gateway",
        "authority",
        "ref_id",
        "content_type",
        "object_id",
        "created_at",
    )

    list_filter = (
        "payment_type",
        "status",
        "gateway",
        "content_type",
    )

    search_fields = (
        "user__username",
        "authority",
        "ref_id",
    )

    autocomplete_fields = (
        "user",

    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "content_type",
    )

    save_on_top = True
    list_per_page = 30

    fieldsets = (
        (_("اطلاعات پرداخت"), {
            "fields": (
                "user",
                "amount",
                "payment_type",
                "status",
                "gateway",
            )
        }),
        (_("اطلاعات درگاه"), {
            "fields": (
                "authority",
                "ref_id",
            ),
            "classes": ("tab",),
        }),
        (_("مرجع پرداخت"), {
            "fields": (
                "content_type",
                "object_id",
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