import graphene
from graphene_subscriptions.events import CREATED, DELETED, UPDATED

from recipes.models import Ingredient, Recipe

from .types import IngredientType, RecipeType


class IngredientSubscription(graphene.ObjectType):
    ingredient_created = graphene.Field(IngredientType)
    ingredient_updated = graphene.Field(IngredientType, id=graphene.Int())
    ingredient_deleted = graphene.Field(IngredientType, id=graphene.Int())

    def resolve_ingredient_created(root, info):
        return root.filter(
            lambda event: event.operation == CREATED
            and isinstance(event.instance, Ingredient)
        ).map(lambda event: event.instance)

    def resolve_ingredient_updated(root, info, id):
        return root.filter(
            lambda event: event.operation == UPDATED
            and isinstance(event.instance, Ingredient)
            and event.instance.pk == id
        ).map(lambda event: event.instance)

    def resolve_ingredient_deleted(root, info, id):
        return root.filter(
            lambda event: event.operation == DELETED
            and isinstance(event.instance, Ingredient)
            and event.instance.pk == id
        ).map(lambda event: event.instance)


class RecipeSubscription(graphene.ObjectType):
    recipe_created = graphene.Field(RecipeType)
    recipe_updated = graphene.Field(RecipeType, id=graphene.Int())
    recipe_deleted = graphene.Field(RecipeType, id=graphene.Int())

    def resolve_recipe_created(root, info):
        return root.filter(
            lambda event: event.operation == CREATED
            and isinstance(event.instance, Recipe)
        ).map(lambda event: event.instance)

    def resolve_recipe_updated(root, info, id):
        return root.filter(
            lambda event: event.operation == UPDATED
            and isinstance(event.instance, Recipe)
            and event.instance.pk == id
        ).map(lambda event: event.instance)

    def resolve_recipe_deleted(root, info, id):
        return root.filter(
            lambda event: event.operation == DELETED
            and isinstance(event.instance, Recipe)
            and event.instance.pk == id
        ).map(lambda event: event.instance)


class Subscription(IngredientSubscription, RecipeSubscription, graphene.ObjectType):
    pass
