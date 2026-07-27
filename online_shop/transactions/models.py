# django built-in
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# local apps
from online_shop.common.models import BaseModel


class TransactionStatus(models.TextChoices):
    PENDING = "pending", _("در انتظار پرداخت")
    CALLBACK_RECEIVED = "callback_received", _("بازگشت از درگاه")
    VERIFIED = "verified", _("تأیید شده")
    FAILED = "failed", _("ناموفق")


class TransactionType(models.TextChoices):
    ORDER = "order", _("پرداخت سفارش")
    WALLET_CHARGE = "wallet_charge", _("شارژ کیف پول")


class EntryType(models.TextChoices):
    PRINCIPAL = "principal", _("مبلغ اصلی")
    COMMISSION = "commission", _("کارمزد")


class Transactioans(BaseModel):
    """
    the main record of transactions
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("کاربر"),
    )

    transaction_type = models.CharField(
        verbose_name=_("نوع تراکنش"),
        max_length=20,
        choices=TransactionType.choices,
    )

    order = models.ForeignKey(
        "users.OrderModel",  
        on_delete=models.SET_NULL,
        related_name="transactions",
        verbose_name=_("سفارش"),
        null=True,
        blank=True,
    )

    gateway = models.CharField(_("درگاه پرداخت"), max_length=50, default="zarinpal")

    authority = models.CharField(
        _("کد پیگیری درگاه (Authority)"),
        max_length=100,
        unique=True,
    )

    ref_id = models.CharField(
        _("شناسه‌ی مرجع تراکنش بانکی"),
        max_length=100,
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("وضعیت"),
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    total_amount = models.PositiveBigIntegerField(
        _("مبلغ کل (ریال)"),
        help_text=_("مجموع تمام ردیف‌ها (مبلغ اصلی + کارمزد)"),
    )

    raw_callback_data = models.JSONField(
        _("پاسخ خام بانک"),
        null=True,
        blank=True,
    )

    verified_at = models.DateTimeField(_("زمان تأیید نهایی"), null=True, blank=True)

    class Meta:
        verbose_name = _("تراکنش")
        verbose_name_plural = _("تراکنش‌ها")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["authority"], name="idx_transaction_authority"),
            models.Index(fields=["status"], name="idx_transaction_status"),
        ]

    def __str__(self) -> str:
        return f"{self.get_transaction_type_display()} - {self.total_amount} - {self.status}"

    def clean(self):
        
        if self.pk:
            entries_sum = self.entries.aggregate(
                total=models.Sum("amount")
            )["total"] or 0
            if entries_sum and entries_sum != self.total_amount:
                raise ValidationError(
                    {
                        "total_amount": _(
                            "مجموع ردیف‌های تراکنش با مبلغ کل همخوانی ندارد."
                        )
                    }
                )


class TransactionEntry(BaseModel):

    transaction = models.ForeignKey(
        Transactioans,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name=_("تراکنش"),
    )

    entry_type = models.CharField(
        _("نوع ردیف"),
        max_length=20,
        choices=EntryType.choices,
    )

    amount = models.PositiveBigIntegerField(_("مبلغ (ریال)"))

    description = models.CharField(
        _("توضیحات"),
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = _("ردیف تراکنش")
        verbose_name_plural = _("ردیف‌های تراکنش")
        ordering = ["-created_at"]
        unique_together = ("transaction", "entry_type")

    def __str__(self) -> str:
        return f"{self.get_entry_type_display()}: {self.amount}"

    def save(self, *args, **kwargs):
        
        if self.pk:
            raise ValidationError(
                _("ردیف‌های تراکنش قابل ویرایش نیستند؛ فقط قابل ایجاد هستند.")
            )
        super().save(*args, **kwargs)