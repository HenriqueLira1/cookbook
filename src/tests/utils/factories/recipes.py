import factory

from recipes.models import Ingredient, Recipe


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Sequence(lambda n: f"Ingredient {n}")


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    title = factory.Sequence(lambda n: f"Recipe {n}")
    cooking_time = factory.Sequence(lambda n: f"{n} minutes")
    image = factory.Sequence(lambda n: f"recipe_{n}.jpeg")


class RecipeWithIngredientsFactory(RecipeFactory):
    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not create:
            return None

        if extracted:
            for ingredient in extracted:
                self.ingredients.add(ingredient)
