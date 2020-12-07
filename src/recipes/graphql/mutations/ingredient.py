import graphene

from recipes.serializers import IngredientSerializer
from shared.constants import (
    CREATE_MODEL_OPERATION,
    DELETE_MODEL_OPERATION,
    UPDATE_MODEL_OPERATION,
)
from shared.graphql import SerializerMutation

from ..types import IngredientType


class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class BaseIngredientMutationMeta:
    arguments = {"input": IngredientInput(required=True)}
    output = IngredientType
    serializer_class = IngredientSerializer


class CreateIngredientMutation(SerializerMutation):
    class Meta(BaseIngredientMutationMeta):
        model_operation = CREATE_MODEL_OPERATION


class UpdateIngredientMutation(SerializerMutation):
    class Meta(BaseIngredientMutationMeta):
        model_operation = UPDATE_MODEL_OPERATION


class DeleteIngredientMutation(SerializerMutation):
    class Meta(BaseIngredientMutationMeta):
        arguments = {"id": graphene.ID(required=True)}
        model_operation = DELETE_MODEL_OPERATION


class IngredientMutations(graphene.ObjectType):
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()
