import graphene

from recipes.serializers import IngredientSerializer
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
        model_operation = "create"


class UpdateIngredientMutation(SerializerMutation):
    class Meta(BaseIngredientMutationMeta):
        model_operation = "update"


class DeleteIngredientMutation(SerializerMutation):
    class Meta(BaseIngredientMutationMeta):
        arguments = {"id": graphene.ID(required=True)}
        model_operation = "delete"


class IngredientMutations(graphene.ObjectType):
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()
