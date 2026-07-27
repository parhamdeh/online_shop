# django built in apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.db.models import F
# local apps
from online_shop.transactions.services import transactions
from online_shop.transactions.models import TransactionType, TransactionStatus
from online_shop.users.selectors.order_selectors import get_order_by_id
from online_shop.users.selectors.user_selectors import get_admin_wallet
from online_shop.payment_gateway.enums import PaymentType, PaymentStatus
from online_shop.payment_gateway.factory import GatewayFactory
from online_shop.payment_gateway.models import PaymentModel
from online_shop.core.exceptions import ApplicationError
from online_shop.users.models import OrderStatus



def create_payment(*, user, data):
    order = get_order_by_id(order_id=data["order_id"])
    return PaymentModel.objects.create(
        user=          user,
        order=         order,
        amount=        data["amount"],
        payment_type=  data["payment_type"],
        status=        PaymentStatus.PENDING,
    )

def call_zarinpal(*, user, data):
    gateway = GatewayFactory.get("zarinpal")
    payment = create_payment(user=user, data=data)
    result = gateway.request(
        {
            "price": payment.amount,
            "description": data["description"],
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
    wallet = payment.user.wallet

    wallet.balance = F("balance") + payment.amount

    wallet.save(update_fields=["balance"])

    fields = {
            "user" : payment.user,
            "transaction_type" : TransactionType.WALLET_CHARGE,
            "gateway" : payment.gateway,
            "ref_id" : payment.ref_id,
            "status" : TransactionStatus.VERIFIED,
            "authority" : payment.authority,
            "commission_amount" : 0,
        }
    
    transactions(fields=fields) 

def order_payment(*, payment: PaymentModel):
    order = payment.order
    order.status = OrderStatus.PAID

    order.save(update_fields=["status"])
    admin_wallet = get_admin_wallet()

    admin_wallet.balance = F("balance") + payment.amount
    admin_wallet.save(update_fields=["balance"])

    fields = {
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

    payment = get_payment_by_authority(
        authority=authority,
    ).select_for_update().get()

    if status != "OK":
        payment.status = PaymentStatus.FAILED
        payment.save(update_fields=["status"])
        raise ApplicationError("Payment canceled.")

    gateway = GatewayFactory.get(payment.gateway)

    result = gateway.verify(
        authority=authority,
        amount=payment.amount,
    )
    payment.status = PaymentStatus.SUCCESS
    payment.ref_id = result["ref_id"]
    payment.paid_at = timezone.now()

    payment.save(
        update_fields=[
            "status",
            "ref_id",
            "paid_at",
        ]
    )
    return check_payment_type(payment=payment)

def refund_payment():
    ...