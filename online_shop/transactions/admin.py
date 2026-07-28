from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm

from online_shop.transactions.models import Transactioans, TransactionEntry


@admin.register(Transactioans)
class TransactionAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm

    list_display = (
        "id",
        "user",
        "transaction_type",
        "total_amount",
        "status",
        "gateway",
        "authority",
    )

    search_fields = (
        "user__username",
        "authority",
        "ref_id",
    )

    ordering = (
        "id",
    )

    list_filter = (
        "transaction_type",
        "status",
        "gateway",
    )

    fieldsets = (
        (_("اطلاعات تراکنش"), {
            "fields": (
                "user",
                "transaction_type",
                "order",
                "gateway",
            )
        }),
        (_("اطلاعات پرداخت"), {
            "fields": (
                "authority",
                "ref_id",
                "status",
                "total_amount",
            )
        }),
        (_("اطلاعات تکمیلی"), {
            "fields": (
                "raw_callback_data",
                "verified_at",
            ),
            "classes": ("collapse",),
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(TransactionEntry)
class TransactionEntryAdmin(ModelAdmin):
    change_password_form = AdminPasswordChangeForm

    list_display = (
        "id",
        "transaction",
        "entry_type",
        "amount",
        "description",
    )

    search_fields = (
        "transaction__authority",
        "transaction__user__username",
        "description",
    )

    ordering = (
        "id",
    )

    list_filter = (
        "entry_type",
    )

    fieldsets = (
        (_("اطلاعات ردیف"), {
            "fields": (
                "transaction",
                "entry_type",
                "amount",
                "description",
            )
        }),
        (_("تاریخ‌ها"), {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )
