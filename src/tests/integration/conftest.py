import pytest
import uuid

from channels.testing import WebsocketCommunicator
from graphene_django.utils.testing import graphql_query
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token
from pytest_factoryboy import register

from tests.utils.factories.recipes import IngredientFactory, RecipeFactory

register(IngredientFactory)
register(RecipeFactory)


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
