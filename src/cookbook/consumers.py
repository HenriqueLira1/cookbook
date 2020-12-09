import json
import logging

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _

from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from graphql_jwt import exceptions
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_user_by_token

logger = logging.getLogger(__name__)


class SubscriptionConsumer(GraphqlSubscriptionConsumer):
    def websocket_receive(self, message):
        user = self.scope.get("user")
        if user is None:
            try:
                token = self._get_token(message)
                self.scope["user"] = self._get_user(token)
            except Exception as error:
                logger.error(error, exc_info=True)
                self.scope["user"] = AnonymousUser()

        return super().websocket_receive(message)

    def _get_user(self, token):
        user = get_user_by_token(token)

        if user is None:
            raise exceptions.JSONWebTokenError(_("User does not exists"))

        if not user.is_authenticated:
            raise exceptions.JSONWebTokenError(_("Invalid authentication credentials"))

        return user

    def _get_token(self, message):
        try:
            request = json.loads(message["text"])
            token = request["payload"]["headers"]["authorization"]
            token_name, token_key = token.split()

            if token_name != jwt_settings.JWT_AUTH_HEADER_PREFIX:
                raise exceptions.JSONWebTokenError(_("Invalid token prefix"))

        except KeyError as error:
            raise exceptions.JSONWebTokenError(_("Token not provided")) from error
        except ValueError as error:
            raise exceptions.JSONWebTokenError(
                _("Token prefix not provided")
            ) from error
        except Exception:
            raise
        else:
            return token_key
