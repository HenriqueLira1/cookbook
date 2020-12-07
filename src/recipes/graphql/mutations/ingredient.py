import graphene

from recipes.serializers import IngredientSerializer
from shared.graphql import SerializerMutation

from ..types import IngredientType


class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class CreateIngredientMutation(SerializerMutation):
    class Meta:
        arguments = {"input": IngredientInput(required=True)}
        output = IngredientType
        serializer_class = IngredientSerializer
        model_operation = "create"


class UpdateIngredientMutation(SerializerMutation):
    class Meta:
        arguments = {"input": IngredientInput(required=True)}
        output = IngredientType
        serializer_class = IngredientSerializer
        model_operation = "update"


class DeleteIngredientMutation(SerializerMutation):
    class Meta:
        arguments = {"id": graphene.ID(required=True)}
        output = IngredientType
        serializer_class = IngredientSerializer
        model_operation = "delete"


class IngredientMutations(graphene.ObjectType):
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()
