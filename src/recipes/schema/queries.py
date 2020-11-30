import graphene

from recipes.models import Ingredient, Recipe

from .types import IngredientType, RecipeType


class Query(graphene.ObjectType):
    ingredients = graphene.List(IngredientType)
    ingredient = graphene.Field(IngredientType, id=graphene.Int())

    recipes = graphene.List(RecipeType)
    recipe = graphene.Field(RecipeType, id=graphene.Int())

    def resolve_ingredients(root, info):
        return Ingredient.objects.order_by("id")

    def resolve_ingredient(root, info, id):
        return Ingredient.objects.get(pk=id)

    def resolve_recipes(root, info):
        return Recipe.objects.order_by("id")

    def resolve_recipe(root, info, id):
        return Recipe.objects.get(pk=id)
