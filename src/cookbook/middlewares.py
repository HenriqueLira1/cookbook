import logging

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _

from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from graphql_jwt import exceptions
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_user_by_token

logger = logging.getLogger(__name__)


class JSONWebTokenMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            token = self._get_token(scope)
            scope["user"] = await sync_to_async(self._get_user)(token)
        except Exception as error:
            logger.error(error, exc_info=True)
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    def _get_user(self, token):
        user = get_user_by_token(token)

        if user is None:
            raise exceptions.JSONWebTokenError(_("User does not exists"))

        if not user.is_authenticated:
            raise exceptions.JSONWebTokenError(_("Invalid authentication credentials"))

        return user

    def _get_token(self, scope):
        try:
            headers = dict(scope["headers"])

            if b"authorization" not in headers:
                raise exceptions.JSONWebTokenError(
                    _("Authentication credentials were not provided")
                )

            token_name, token_key = headers[b"authorization"].decode().split()

            if token_name != jwt_settings.JWT_AUTH_HEADER_PREFIX:
                raise exceptions.JSONWebTokenError(_("Invalid token prefix"))

        except ValueError as error:
            raise exceptions.JSONWebTokenError(
                _("Token prefix not provided")
            ) from error
        except exceptions.JSONWebTokenError:
            raise
        else:
            return token_key


def JSONWebTokenMiddlewareStack(inner):
    return JSONWebTokenMiddleware(AuthMiddlewareStack(inner))
