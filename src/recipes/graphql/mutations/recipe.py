import graphene

from recipes.serializers import RecipeSerializer
from shared.graphql import SerializerMutation

from ..types import RecipeType


class RecipeInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    cooking_time = graphene.String()
    image = graphene.String()
    ingredients = graphene.List(graphene.Int)


class CreateRecipeMutation(SerializerMutation):
    class Meta:
        arguments = {"input": RecipeInput(required=True)}
        output = RecipeType
        serializer_class = RecipeSerializer
        model_operation = "create"


class UpdateRecipeMutation(SerializerMutation):
    class Meta:
        arguments = {"input": RecipeInput(required=True)}
        output = RecipeType
        serializer_class = RecipeSerializer
        model_operation = "update"


class DeleteRecipeMutation(SerializerMutation):
    class Meta:
        arguments = {"id": graphene.ID(required=True)}
        output = RecipeType
        serializer_class = RecipeSerializer
        model_operation = "delete"


class RecipeMutations(graphene.ObjectType):
    create_recipe = CreateRecipeMutation.Field()
    update_recipe = UpdateRecipeMutation.Field()
    delete_recipe = DeleteRecipeMutation.Field()
