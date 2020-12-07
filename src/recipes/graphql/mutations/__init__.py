import graphene

from .ingredient import IngredientMutations
from .recipe import RecipeMutations


class Mutation(IngredientMutations, RecipeMutations, graphene.ObjectType):
    pass
