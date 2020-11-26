import graphene
import graphene_django

from .models import Ingredient, Recipe


class IngredientType(graphene_django.DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeType(graphene_django.DjangoObjectType):
    class Meta:
        model = Recipe
        fields = "__all__"


class Query(graphene.ObjectType):
    ingredients = graphene_django.DjangoListField(IngredientType)
    ingredient = graphene.Field(IngredientType, id=graphene.Int())

    recipes = graphene_django.DjangoListField(RecipeType)
    recipe = graphene.Field(RecipeType, id=graphene.Int())

    def resolve_ingredient(root, info, id):
        return Ingredient.objects.get(pk=id)

    def resolve_recipe(root, info, id):
        return Recipe.objects.get(pk=id)
