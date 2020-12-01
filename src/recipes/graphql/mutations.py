from django.shortcuts import get_object_or_404

import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from recipes.models import Ingredient, Recipe
from recipes.serializers import IngredientSerializer, RecipeSerializer

from .types import IngredientType, RecipeType


class CreateIngredientMutation(SerializerMutation):
    class Meta:
        serializer_class = IngredientSerializer
        model_operations = ["create"]


class UpdateIngredientMutation(SerializerMutation):
    class Meta:
        serializer_class = IngredientSerializer
        model_operations = ["update"]


class DeleteIngredientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = IngredientType

    def mutate(root, info, id):
        instance = get_object_or_404(Ingredient, pk=id)
        instance.delete()

        return instance


class RecipeInput(graphene.InputObjectType):
    id = graphene.Int()
    title = graphene.String()
    cooking_time = graphene.String()
    image = graphene.String()
    ingredients = graphene.List(graphene.Int)


class CreateRecipeMutation(graphene.Mutation):
    class Arguments:
        input = RecipeInput(required=True)

    Output = RecipeType

    def mutate(root, info, input):
        serializer = RecipeSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        return serializer.save()


class UpdateRecipeMutation(graphene.Mutation):
    class Arguments:
        input = RecipeInput(required=True)

    Output = RecipeType

    def mutate(root, info, input):
        instance = get_object_or_404(Recipe, pk=input.get("id"))
        serializer = RecipeSerializer(instance, data=input, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()


class DeleteRecipeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = RecipeType

    def mutate(root, info, id):
        instance = get_object_or_404(Recipe, pk=id)
        instance.delete()

        return instance


class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()

    create_recipe = CreateRecipeMutation.Field()
    update_recipe = UpdateRecipeMutation.Field()
    delete_recipe = DeleteRecipeMutation.Field()