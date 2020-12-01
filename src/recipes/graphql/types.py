import graphene_django

from recipes.models import Ingredient, Recipe


class IngredientType(graphene_django.DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeType(graphene_django.DjangoObjectType):
    class Meta:
        model = Recipe
        fields = "__all__"
