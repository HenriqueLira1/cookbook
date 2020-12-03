import pytest
import uuid

from django.db.models.signals import post_delete, post_save

from channels.testing import WebsocketCommunicator
from graphene_django.utils.testing import graphql_query
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from graphene_subscriptions.signals import (
    post_delete_subscription,
    post_save_subscription,
)
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token
from pytest_factoryboy import register

from tests.utils.factories.recipes import (
    IngredientFactory,
    RecipeFactory,
    RecipeWithIngredientsFactory,
)

register(IngredientFactory)
register(RecipeFactory)
register(RecipeWithIngredientsFactory)


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client_with_credentials(db, client, create_user):
    def func(*args, **kwargs):
        user = create_user()
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {get_token(user)}"
            )
        }
        return graphql_query(*args, **kwargs, client=client, headers=headers)

    return func


@pytest.fixture
async def websocket_communicator():
    communicator = WebsocketCommunicator(
        GraphqlSubscriptionConsumer.as_asgi(), "/graphql/"
    )
    connected, subprotocol = await communicator.connect()
    assert connected
    yield communicator
    await communicator.disconnect()


@pytest.fixture
def execute_websocket_query(websocket_communicator):
    async def func(query, variables=None):
        await websocket_communicator.send_json_to(
            {
                "id": 1,
                "type": "start",
                "payload": {"query": query, "variables": variables},
            }
        )

    return func


@pytest.fixture
def connect_post_save_signal():
    def func(sender_instance):
        dispatch_uid = f"{sender_instance.__class__.__name__}_post_save"

        yield post_save.connect(
            post_save_subscription, sender=sender_instance, dispatch_uid=dispatch_uid
        )
        post_save.disconnect(
            post_save_subscription, sender=sender_instance, dispatch_uid=dispatch_uid
        )

    return func


@pytest.fixture
def connect_post_delete_signal():
    def func(sender_instance):
        dispatch_uid = f"{sender_instance.__class__.__name__}_post_delete"

        yield post_delete.connect(
            post_delete_subscription, sender=sender_instance, dispatch_uid=dispatch_uid
        )
        post_delete.disconnect(
            post_delete_subscription, sender=sender_instance, dispatch_uid=dispatch_uid
        )

    return func
