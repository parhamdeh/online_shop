from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WalletConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = f"wallet_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def wallet_balance(self, event):

        await self.send_json(event["data"])