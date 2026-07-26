from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from online_shop.common.models import BaseModel
from online_shop.users.models import BaseUserModel
from online_shop.payment_gateway.enums import PaymentStatus, PaymentType



class PaymentGateway(models.TextChoices):
    ZARINPAL = "zarinpal", "ZarinPal"


class PaymentModel(BaseModel):
    """
    Stores payment requests and their gateway responses.

    A payment may be associated with different business objects such as
    an order or a wallet charge through a GenericForeignKey.
    """

    user = models.ForeignKey(
        BaseUserModel,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="کاربر",
        help_text="کاربری که این پرداخت را ایجاد کرده است.",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="مبلغ",
        help_text="مبلغ پرداخت.",
    )

    payment_type = models.CharField(
        max_length=30,
        choices=PaymentType.choices,
        verbose_name="نوع پرداخت",
        help_text="مشخص می‌کند پرداخت مربوط به سفارش یا شارژ کیف پول است.",
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="وضعیت پرداخت",
        help_text="وضعیت فعلی پرداخت.",
    )

    gateway = models.CharField(
        max_length=30,
        choices=PaymentGateway.choices,
        default=PaymentGateway.ZARINPAL,
        verbose_name="درگاه پرداخت",
        help_text="درگاه مورد استفاده برای انجام پرداخت.",
    )

    authority = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Authority",
        help_text="شناسه Authority دریافتی از درگاه پرداخت.",
    )

    ref_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="شماره مرجع",
        help_text="شماره مرجع (Ref ID) پس از پرداخت موفق.",
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        verbose_name="نوع مرجع",
        help_text="نوع موجودیتی که این پرداخت به آن تعلق دارد.",
    )

    object_id = models.PositiveBigIntegerField(
        verbose_name="شناسه مرجع",
        help_text="شناسه موجودیت مرتبط با این پرداخت.",
    )

    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Payment #{self.pk} - {self.user}"