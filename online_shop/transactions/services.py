# local apps
from online_shop.users.selectors.user_selectors import get_user_by_id, get_user_wallet
from online_shop.users.models import UserWallet
from online_shop.transactions.models import Transactioans, EntryType, TransactionEntry
# django built in apps
from django.db import transaction

def create_transaction(*, fields: dict) -> Transactioans:
    order = fields["order"]
    if fields["transaction_type"] == "order":
        total_amount = order.total_price + fields['commission_amount']
    else: 
        total_amount = fields["balance"]
        

    transaction = Transactioans.objects.create(
        user=fields['user'],
        transaction_type=fields["transaction_type"],
        order=order,
        gateway=fields["gateway"],
        ref_id=fields["ref_id"],
        status=fields["status"],
        authority=fields['authority'],
        total_amount=total_amount,
    )
    return transaction

def create_transaction_entry_principal(*, transaction: Transactioans) -> TransactionEntry:

    if transaction.transaction_type == "order":
        amount = transaction.order.total_price 
    else: 
        amount = transaction.total_amount

    return TransactionEntry.objects.create(
        transaction=transaction,
        entry_type=EntryType.PRINCIPAL,
        amount=amount,
        description="this is for principal",
    )

def create_transaction_entry_commission(*, transaction: Transactioans) -> TransactionEntry:
    # if transaction.transaction_type == "order":
    #         amount = transaction.order.total_price 
    # else: 
    #     amount = transaction.total_amount
    return TransactionEntry.objects.create(
            transaction=transaction,
            entry_type=EntryType.COMMISSION,
            amount=0,
            description="this is for commission",
        )

@transaction.atomic
def transactions(*, fields: dict) -> Transactioans:
    transaction = create_transaction(fields=fields)
    create_transaction_entry_commission(transaction=transaction)
    create_transaction_entry_principal(transaction=transaction)

def rebuild_wallet_balance(user_id: int) -> UserWallet:
    user = get_user_by_id(user_id=user_id)
    wallet = get_user_wallet(user=user)

    Transactioans.objects.filter(user=user).all()


