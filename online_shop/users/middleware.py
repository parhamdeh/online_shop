from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from online_shop.users.models import BaseUserModel


@database_sync_to_async
def get_user(user_id: int):
    try:
        return BaseUserModel.objects.get(id=user_id)
    except BaseUserModel.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Authenticate websocket connections using SimpleJWT access token.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        query = parse_qs(scope["query_string"].decode())

        token = query.get("token")

        if not token:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        token = token[0]

        try:
            access = AccessToken(token)

            user = await get_user(access["user_id"])

            scope["user"] = user

        except TokenError:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)