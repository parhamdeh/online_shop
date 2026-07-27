# local apps
from online_shop.transactions.models import Transactioans, EntryType, TransactionEntry
# django built in apps
from django.db import transaction

def create_transaction(*, fields: dict) -> Transactioans:
    order = fields['order']
    transaction = Transactioans.objects.create(
        user=fields['user'],
        transaction_type=fields["transaction_type"],
        order=order,
        gateway=fields["gateway"],
        ref_id=fields["ref_id"],
        status=fields["status"],
        authority=fields['authority'],
        total_amount=order.total_price + fields['commission_amount'],
    )
    return transaction

def create_transaction_entry_principal(*, transaction: Transactioans) -> TransactionEntry:
    return TransactionEntry.objects.create(
        transaction=transaction,
        entry_type=EntryType.PRINCIPAL,
        amount=transaction.order.total_price,
        description="this is for principal",
    )

def create_transaction_entry_commission(*, transaction: Transactioans) -> TransactionEntry:
    return TransactionEntry.objects.create(
            transaction=transaction,
            entry_type=EntryType.COMMISSION,
            amount=transaction.order.total_price,
            description="this is for commission",
        )

@transaction.atomic
def transactions(*, fields: dict) -> Transactioans:
    transaction = create_transaction(fields=fields)
    create_transaction_entry_commission(transaction=transaction)
    create_transaction_entry_principal(transaction=transaction)
    