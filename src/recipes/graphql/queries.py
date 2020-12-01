import graphene
from graphql_jwt.decorators import login_required

from recipes.models import Ingredient, Recipe

from .types import IngredientType, RecipeType


class IngredientQuery(graphene.ObjectType):
    ingredients = graphene.List(IngredientType)
    ingredient = graphene.Field(IngredientType, id=graphene.Int())

    @login_required
    def resolve_ingredients(root, info):
        return Ingredient.objects.order_by("id")

    @login_required
    def resolve_ingredient(root, info, id):
        print(info.context.user)
        return Ingredient.objects.get(pk=id)


class RecipeQuery(graphene.ObjectType):
    recipes = graphene.List(RecipeType)
    recipe = graphene.Field(RecipeType, id=graphene.Int())

    @login_required
    def resolve_recipes(root, info):
        return Recipe.objects.order_by("id")

    @login_required
    def resolve_recipe(root, info, id):
        return Recipe.objects.get(pk=id)


class Query(IngredientQuery, RecipeQuery, graphene.ObjectType):
    pass
