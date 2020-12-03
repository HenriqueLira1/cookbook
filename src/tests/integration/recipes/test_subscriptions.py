import pytest

from asgiref.sync import sync_to_async

from recipes.models import Ingredient


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_created_subscription(
    websocket_communicator, execute_websocket_query, connect_post_save_signal
):
    connect_post_save_signal(Ingredient)

    await execute_websocket_query(
        """
            subscription {
                ingredientCreated {
                    name
                }
            }
        """
    )

    ingredient = await sync_to_async(Ingredient.objects.create)(name="Chocolate")

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"ingredientCreated": {"name": ingredient.name}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_updated_subscription(
    websocket_communicator, execute_websocket_query, connect_post_save_signal
):
    connect_post_save_signal(Ingredient)

    ingredient = await sync_to_async(Ingredient.objects.create)(name="Rice")

    await execute_websocket_query(
        """
            subscription IngredientUpdated($id: ID!) {
                ingredientUpdated(id: $id) {
                    name
                }
            }
        """,
        variables={"id": ingredient.pk},
    )

    ingredient.name = "Beans"
    await sync_to_async(ingredient.save)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"ingredientUpdated": {"name": "Beans"}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_deleted_subscription(
    websocket_communicator, execute_websocket_query, connect_post_delete_signal
):
    connect_post_delete_signal(Ingredient)

    ingredient = await sync_to_async(Ingredient.objects.create)(name="Chocolate")

    await execute_websocket_query(
        """
            subscription IngredientDeleted($id: ID!) {
                ingredientDeleted(id: $id) {
                    name
                }
            }
        """,
        variables={"id": ingredient.pk},
    )

    await sync_to_async(ingredient.delete)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"ingredientDeleted": {"name": ingredient.name}},
        "errors": None,
    }
