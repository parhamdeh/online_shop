#third party
from typing import Any
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta

# django built in apps
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager as BUM
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# local apps
from online_shop.products.models import ProductsModel
from online_shop.common.models import BaseModel
from online_shop.products.models import ProductsModel



class BaseUserManager(BUM):
    """
    custom manger for handle BaseUserModel 
    """
    use_in_migrations = True

    def _create_user_object(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, username, password, **extra_fields):
        user = self._create_user_object(username, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        
        return self._create_user(username, password, **extra_fields)

    create_user.alters_data = True
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(username, password, **extra_fields)

    create_superuser.alters_data = True



class BaseUserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    custom user model 
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_("نام کاربری"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone = PhoneNumberField(
        unique=True,
        region="IR",
        verbose_name=_("شماره تلفن ")
    )
    is_staff = models.BooleanField(default=False, verbose_name=_("ادمین است"))
    is_active = models.BooleanField(default=False, verbose_name=_("فعال است"))
    

    objects = BaseUserManager()

   
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربر")

    def __str__(self):
        return f"{self.phone} ({self.username})"


class ProfileModel(BaseModel):
    """
    Model for handle user profile and users info
    """
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_profile", verbose_name=_("کاربر"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("پروفایل کاربر")
        verbose_name_plural = _("پروفایل کاربر")
    

class CartModel(BaseModel):
    """
    shoping cart for handle user's targets
    """
    user = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE, related_name="user_cart", verbose_name=_("کاربر"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _(" سبد خرید")
        verbose_name_plural = _("سبد خرید ")
        

class UserOrder(BaseModel):
    """
    model for handle user orders 
    """
    user = models.ForeignKey(BaseUserModel, on_delete=models.PROTECT, related_name="user_order", verbose_name=_("کاربر"))
    product = models.ForeignKey(ProductsModel, on_delete=models.PROTECT, related_name="product", verbose_name=_("محصول"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _(" سفارش")
        verbose_name_plural = _("سفارش")
    
    def __str__(self):
        return f"order {self.product.title} for {self.user.username}"


class UserWallet(BaseModel):
    balance = models.PositiveIntegerField(default=0, verbose_name=_("موجودی به ریال"))
    user = models.OneToOneField(BaseUserModel, on_delete=models.PROTECT, related_name="user_wallet", verbose_name=_("کاربر"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _(" کیف پول")
        verbose_name_plural = _("کیف پول")
    
    def __str__(self):
        return f"wallet for {self.user.username} with {self.balance} rials balance"


class OtpModel(BaseModel):
    """
    model for otp codes becuase cache didnt work
    """

    phone = PhoneNumberField(region="IR")
    code = models.CharField()


class CartItemModel(BaseModel):
    cart = models.ForeignKey(
        CartModel,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_("سبد خرید")
    )

    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        verbose_name=_("محصول")
    )

    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name=_("تعداد محصولات"))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _(" سبد ")
        verbose_name_plural = _("سبد ")