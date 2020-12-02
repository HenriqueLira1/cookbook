from rest_framework import status

from recipes.models import Ingredient, Recipe


def test_create_ingredient_mutation(api_client_with_credentials):
    response = api_client_with_credentials(
        """
        mutation CreateIngredient($input: IngredientInput!) {
            ingredient: createIngredient(input: $input) {
                id
                name
            }
        }
        """,
        input_data={"id": 1, "name": "Chocolate"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Ingredient.objects.get(pk=1).name == "Chocolate"


def test_update_ingredient_mutation(api_client_with_credentials, ingredient_factory):
    ingredient_factory.create(id=1, name="Rice")

    response = api_client_with_credentials(
        """
        mutation UpdateIngredient($input: IngredientInput!) {
            ingredient: updateIngredient(input: $input) {
                id
                name
            }
        }
        """,
        input_data={"id": 1, "name": "Beans"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Ingredient.objects.get(pk=1).name == "Beans"


def test_delete_ingredient_mutation(api_client_with_credentials, ingredient_factory):
    ingredient_factory.create(id=1)

    response = api_client_with_credentials(
        """
        mutation DeleteIngredient($id: ID!) {
            ingredient: deleteIngredient(id: $id) {
                name
            }
        }
        """,
        variables={"id": 1},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Ingredient.objects.count() == 0


def test_create_recipe_mutation(api_client_with_credentials, ingredient_factory):
    ingredients = ingredient_factory.create_batch(2)

    response = api_client_with_credentials(
        """
        mutation CreateRecipe($input: RecipeInput!) {
            recipe: createRecipe(input: $input) {
                title
                cookingTime
                image
                ingredients {
                    id
                }
            }
        }
        """,
        input_data={
            "id": 1,
            "title": "Amazing Recipe",
            "cookingTime": "10 minutes",
            "image": "recipe.jpg",
            "ingredients": [ingredient.id for ingredient in ingredients],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert Recipe.objects.get(pk=1).title == "Amazing Recipe"


def test_update_recipe_mutation(api_client_with_credentials, recipe_factory):
    recipe_factory.create(id=1, title="Amazing Recipe")

    response = api_client_with_credentials(
        """
        mutation UpdateRecipe($input: RecipeInput!) {
            recipe: updateRecipe(input: $input) {
                id
                title
            }
        }
        """,
        input_data={"id": 1, "title": "Second most amazing recipe"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Recipe.objects.get(pk=1).title == "Second most amazing recipe"


def test_delete_recipe_mutation(api_client_with_credentials, recipe_factory):
    recipe_factory.create(id=1)

    response = api_client_with_credentials(
        """
        mutation DeleteRecipe($id: ID!) {
            recipe: deleteRecipe(id: $id) {
                id
                title
            }
        }
        """,
        variables={"id": 1},
    )

    assert response.status_code == status.HTTP_200_OK
    assert Recipe.objects.count() == 0
