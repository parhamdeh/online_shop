from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_wallet_balance(
    *,
    user_id: int,
    balance,
):

    channel_layer = get_channel_layer()

    async_to_sync(
        channel_layer.group_send
    )(
        f"wallet_{user_id}",
        {
            "type": "wallet_balance",
            "data": {
                "balance": str(balance),
            },
        },
    )