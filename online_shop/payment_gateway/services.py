# django built in apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.db.models import F
# local apps
from online_shop.users.websocket import send_wallet_balance
from online_shop.transactions.services import transactions
from online_shop.transactions.models import TransactionType, TransactionStatus
from online_shop.users.selectors.order_selectors import get_order_by_id
from online_shop.users.selectors.user_selectors import get_admin_wallet
from online_shop.payment_gateway.enums import PaymentType, PaymentStatus
from online_shop.payment_gateway.factory import GatewayFactory
from online_shop.payment_gateway.models import PaymentModel
from online_shop.core.exceptions import ApplicationError
from online_shop.users.models import BaseUserModel, OrderStatus, UserWallet



def check_content_object(*, user: BaseUserModel, data: dict):
    """
    Return the target object associated with the requested payment.

    Depending on the payment type, this function returns either the
    user's order or the user's wallet. The returned object is later
    attached to the payment as its content object.

    Args:
        user: The authenticated user.
        data: Validated payment request data.

    Returns:
        OrderModel | WalletModel:
            The object associated with the payment.
    """
    if data["payment_type"] == PaymentType.ORDER:
        return get_order_by_id(order_id=data["order_id"], user=user).get()
    else:
        return user.user_wallet

def create_payment(*, user, data):
    """
    Create a new payment record.

    If the payment is for an order, the payment amount is automatically
    calculated from the order's total price.

    Args:
        user: The authenticated user.
        data: Validated payment request data.

    Returns:
        PaymentModel:
            The newly created payment instance.
    """
    content_object = check_content_object(data=data, user=user)
    if data["payment_type"] == PaymentType.ORDER:
        data["amount"] = content_object.total_price
    
    return PaymentModel.objects.create(
        user=           user,
        amount=         int(data["amount"]),
        payment_type=   data["payment_type"],
        status=         PaymentStatus.PENDING,
        content_object= content_object,
    )

def call_zarinpal(*, user, data):
    """
    Create a payment and send a payment request to Zarinpal.

    After creating the payment record, this function requests a payment
    session from the gateway, stores the generated authority code,
    and returns the payment URL.

    Args:
        user: The authenticated user.
        data: Validated payment request data.

    Returns:
        dict:
            Dictionary containing the authority code and payment URL.
    """ 

    gateway = GatewayFactory.get("zarinpal")
    payment = create_payment(user=user, data=data)
    result = gateway.request(
        payment={
            "price": payment.amount,
            "description": "buy from zarinpal",
            "phone": user.phone,
        }
    )

    payment.authority = result["authority"]

    payment.save(update_fields=["authority"])

    return {
        "authority": payment.authority,
        "payment_url": result["payment_url"],
    }
    
def wallet_charge(*, payment: PaymentModel):
    """
    Charge the user's wallet after a successful payment.

    This function updates the wallet balance, sends a real-time wallet
    notification through WebSocket, and records the transaction.

    Args:
        payment: A verified payment instance.

    Returns:
        None
    """
    wallet = payment.user.user_wallet

    wallet.balance = F("balance") + payment.amount

    wallet.save(update_fields=["balance"])
    wallet.refresh_from_db()
    send_wallet_balance(
        user_id=payment.user.id,
        balance=wallet.balance,
    )

    fields = {
            "order": None,
            "user" : payment.user,
            "transaction_type" : TransactionType.WALLET_CHARGE,
            "gateway" : payment.gateway,
            "ref_id" : payment.ref_id,
            "status" : TransactionStatus.VERIFIED,
            "authority" : payment.authority,
            "commission_amount" : 0,
            "balance" : payment.amount,
        }
    
    transactions(fields=fields) 

def order_payment(*, payment: PaymentModel):
    
    """
    Complete an order payment.

    Marks the order as paid, transfers the payment amount to the
    administrator wallet, and creates a transaction record.

    Args:
        payment: A verified payment instance.

    Returns:
        None
    """
    order = payment.content_object
    order.status = OrderStatus.PAID

    order.save(update_fields=["status"])
    admin_wallet = get_admin_wallet()

    admin_wallet.balance = F("balance") + payment.amount
    admin_wallet.save(update_fields=["balance"])

    fields = {
        "order": order,
        "user" : payment.user,
        "transaction_type" : TransactionType.ORDER,
        "gateway" : payment.gateway,
        "ref_id" : payment.ref_id,
        "status" : TransactionStatus.VERIFIED,
        "authority" : payment.authority,
        "commission_amount" : 0,
    }

    transactions(fields=fields) 
    
def check_payment_type(*, payment: PaymentModel):
    """
    Execute the appropriate payment workflow.

    Depending on the payment type, either charges the user's wallet
    or completes an order payment.

    Args:
        payment: A verified payment instance.

    Returns:
        Any:
            The result of the executed payment handler.
    """
    payment_type = payment.payment_type

    if payment_type == PaymentType.ORDER:
        return order_payment(payment=payment)

    else:
        return wallet_charge(payment=payment)

def get_payment_by_authority(*, authority) -> PaymentModel:
    return PaymentModel.objects.filter(
        authority=authority,
    )

@transaction.atomic
def verify_payment(*, authority: str, status: str, user):
    """
    Retrieve a payment by its authority code.

    Args:
        authority: Gateway authority code.

    Returns:
        QuerySet[PaymentModel]:
            QuerySet containing the matching payment.
    """

    payment = get_payment_by_authority(
        authority=authority,
    ).select_for_update().get()

    if status != "OK":
        payment.status = PaymentStatus.FAILED
        payment.save(update_fields=["status"])
        raise ApplicationError("Payment canceled.")

    gateway = GatewayFactory.get(payment.gateway)

    result = gateway.verify(
        payment=payment
    )
    payment.status = PaymentStatus.SUCCESS
    payment.ref_id = result["ref_id"]
    payment.paid_at = timezone.now()

    payment.save(
        update_fields=[
            "status",
            "ref_id",
        ]
    )
    return check_payment_type(payment=payment)

@transaction.atomic
def use_wallet_for_buy_product(*, order_id: int, user: BaseUserModel):
    """
    Verify a payment through the payment gateway.

    The payment is locked during verification to prevent concurrent
    modifications. If verification succeeds, the payment information
    is updated and the corresponding business logic is executed.

    Args:
        authority: Gateway authority code.
        status: Payment status returned by the gateway.
        user: The authenticated user.

    Returns:
        Any:
            Result of the payment processing operation.

    Raises:
        ApplicationError:
            If the payment is canceled by the user.
    """
    try:
        order = (
            get_order_by_id(
                order_id=order_id,
                user=user,
            )
            .select_for_update()
            .get()
        )

        admin_wallet = (
            get_admin_wallet()
            .__class__
            .objects.select_for_update()
            .get(pk=get_admin_wallet().pk)
        )

        wallet = (
            UserWallet.objects
            .select_for_update()
            .get(user=user)
        )

    except Exception as ex:
        raise ApplicationError(str(ex))

    if order.status == OrderStatus.PAID:
        raise ApplicationError("Order has already been paid.")

    price = order.total_price

    updated = (
        UserWallet.objects
        .filter(
            pk=wallet.pk,
            balance__gte=price,
        )
        .update(
            balance=F("balance") - price,
        )
    )

    if updated == 0:
        raise ApplicationError("Insufficient wallet balance.")

    UserWallet.objects.filter(
        pk=admin_wallet.pk,
    ).update(
        balance=F("balance") + price,
    )

    order.status = OrderStatus.PAID
    order.save(update_fields=["status"])

    wallet.refresh_from_db()

    send_wallet_balance(
        user_id=user.id,
        balance=wallet.balance,
    )

    transactions(
        fields={
            "order": order,
            "user": user,
            "transaction_type": TransactionType.ORDER,
            "status": TransactionStatus.VERIFIED,
            "gateway": "transaction with wallet",
            "commission_amount": 0,
            "ref_id": None,
            "authority": "transaction with wallet",
        }
    )

    return wallet