# django built in apps
from django.conf import settings
# local apps
from online_shop.payment_gateway.enums import PaymentType, PaymentStatus
from online_shop.payment_gateway.factory import GatewayFactory
from online_shop.payment_gateway.models import PaymentModel


def create_payment(*, user, data):
    

    
    payment = PaymentModel.objects.create(
        user=user,
        order=order,
        amount=amount,
        payment_type=payment_type,
        status=PaymentStatus.PENDING,
    )

    gateway = GatewayFactory.get("zarinpal")

    result = gateway.request(
        {
            "price": payment.amount,
            "description": description,
            "phone": user.phone,
        }
    )

    payment.authority = result["authority"]

    payment.save(update_fields=["authority"])

    return {
        "authority": payment.authority,
        "payment_url": result["payment_url"],
    }

def wallet_charge(*, user, data):
    ...

def check_payment_type(*, user, data):
    payment_type = data["payment_type"]
    
    if payment_type == PaymentType.ORDER:
        ...

        data["amount"] = order.total_price

        data["description"] = f"Order #{order.id}"

    else:
        data['description'] = "Wallet Charge"
        return wallet_charge(user=user, data=data)



def verify_payment():
    ...

def order_payment():
    ...

def refund_payment():
    ...