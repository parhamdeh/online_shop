from django.db import models


class PaymentType(models.TextChoices):
    ORDER = "ORDER", "Order"
    WALLET_CHARGE = "WALLET_CHARGE", "Wallet Charge"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    CANCELED = "CANCELED", "Canceled"