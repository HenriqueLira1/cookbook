from rest_framework import status


def test_ingredients_query(api_client_with_credentials, ingredient_factory):
    ingredient_factory.create_batch(2)

    response = api_client_with_credentials(
        """
        query {
            ingredients {
                id
                name
            }
        }
        """,
    )

    response_content = response.json()["data"]["ingredients"]

    assert response.status_code == status.HTTP_200_OK
    assert len(response_content) == 2


def test_ingredient_query(api_client_with_credentials, ingredient_factory):
    ingredient_factory.create(id=1)

    response = api_client_with_credentials(
        """
        query Ingredients($id: ID!){
            ingredient(id: $id) {
                id
                name
            }
        }
        """,
        variables={"id": 1},
    )

    response_content = response.json()["data"]["ingredient"]

    assert response.status_code == status.HTTP_200_OK
    assert response_content["id"] == "1"


def test_recipes_query(api_client_with_credentials, recipe_with_ingredients_factory):
    recipe_with_ingredients_factory.create_batch(2)

    response = api_client_with_credentials(
        """
        query {
            recipes {
                id
                title
                cookingTime
                image
                ingredients {
                    id
                    name
                }
            }
        }
        """
    )

    response_content = response.json()["data"]["recipes"]

    assert response.status_code == status.HTTP_200_OK
    assert len(response_content) == 2


def test_recipe_query(
    api_client_with_credentials, ingredient_factory, recipe_with_ingredients_factory
):
    ingredients = ingredient_factory.create_batch(2)
    recipe_with_ingredients_factory.create(id=1, ingredients=ingredients)

    response = api_client_with_credentials(
        """
        query Recipe($id: ID!) {
            recipe(id: $id) {
                id
                title
                cookingTime
                image
                ingredients {
                    id
                    name
                }
            }
        }
        """,
        variables={"id": 1},
    )

    response_content = response.json()["data"]["recipe"]

    assert response.status_code == status.HTTP_200_OK
    assert response_content["id"] == "1"
    assert len(response_content["ingredients"]) == 2
