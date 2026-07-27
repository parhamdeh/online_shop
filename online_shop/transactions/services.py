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

def create_transaction_entry_principal(*, fields: dict) -> TransactionEntry:
    ...

def create_transaction_entry_commission(*, fields: dict) -> TransactionEntry:
    ...

@transaction.atomic
def transactions(*, fields: dict) -> Transactioans:
    transaction = create_transaction(fields=fields)
    create_transaction_entry_commission(fields=fields)
    create_transaction_entry_principal(fields=fields)
