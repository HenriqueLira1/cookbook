import graphene

from recipes.serializers import RecipeSerializer
from shared.constants import (
    CREATE_MODEL_OPERATION,
    DELETE_MODEL_OPERATION,
    UPDATE_MODEL_OPERATION,
)
from shared.graphql import SerializerMutation

from ..types import RecipeType


class RecipeInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    cooking_time = graphene.String()
    image = graphene.String()
    ingredients = graphene.List(graphene.Int)


class BaseRecipeMutationMeta:
    arguments = {"input": RecipeInput(required=True)}
    output = RecipeType
    serializer_class = RecipeSerializer


class CreateRecipeMutation(SerializerMutation):
    class Meta(BaseRecipeMutationMeta):
        model_operation = CREATE_MODEL_OPERATION


class UpdateRecipeMutation(SerializerMutation):
    class Meta(BaseRecipeMutationMeta):
        model_operation = UPDATE_MODEL_OPERATION


class DeleteRecipeMutation(SerializerMutation):
    class Meta(BaseRecipeMutationMeta):
        arguments = {"id": graphene.ID(required=True)}
        model_operation = DELETE_MODEL_OPERATION


class RecipeMutations(graphene.ObjectType):
    create_recipe = CreateRecipeMutation.Field()
    update_recipe = UpdateRecipeMutation.Field()
    delete_recipe = DeleteRecipeMutation.Field()
