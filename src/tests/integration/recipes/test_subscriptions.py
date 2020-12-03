import pytest

from asgiref.sync import sync_to_async

from recipes.models import Ingredient, Recipe


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_created_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_save_signal,
    ingredient_factory,
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

    ingredient = await sync_to_async(ingredient_factory.create)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"ingredientCreated": {"name": ingredient.name}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_updated_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_save_signal,
    ingredient_factory,
):
    connect_post_save_signal(Ingredient)

    ingredient = await sync_to_async(ingredient_factory.create)()

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

    ingredient.name = "Chocolate"
    await sync_to_async(ingredient.save)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"ingredientUpdated": {"name": "Chocolate"}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ingredient_deleted_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_delete_signal,
    ingredient_factory,
):
    connect_post_delete_signal(Ingredient)

    ingredient = await sync_to_async(ingredient_factory.create)()

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


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_recipe_created_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_save_signal,
    recipe_factory,
):
    connect_post_save_signal(Recipe)

    await execute_websocket_query(
        """
            subscription {
                recipeCreated {
                    title
                }
            }
        """
    )

    recipe = await sync_to_async(recipe_factory.create)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"recipeCreated": {"title": recipe.title}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_recipe_updated_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_save_signal,
    recipe_factory,
):
    connect_post_save_signal(Recipe)

    recipe = await sync_to_async(recipe_factory.create)()

    await execute_websocket_query(
        """
            subscription RecipeUpdated($id: ID!) {
                recipeUpdated(id: $id) {
                    title
                }
            }
        """,
        variables={"id": recipe.pk},
    )

    recipe.title = "Amazing recipe"
    await sync_to_async(recipe.save)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"recipeUpdated": {"title": "Amazing recipe"}},
        "errors": None,
    }


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_recipe_deleted_subscription(
    websocket_communicator,
    execute_websocket_query,
    connect_post_save_signal,
    recipe_factory,
):
    connect_post_save_signal(Recipe)

    recipe = await sync_to_async(recipe_factory.create)()

    await execute_websocket_query(
        """
            subscription RecipeDeleted($id: ID!) {
                recipeDeleted(id: $id) {
                    title
                }
            }
        """,
        variables={"id": recipe.pk},
    )

    await sync_to_async(recipe.delete)()

    response = await websocket_communicator.receive_json_from()

    assert response["payload"] == {
        "data": {"recipeDeleted": {"title": recipe.title}},
        "errors": None,
    }
