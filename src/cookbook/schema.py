from graphene import ObjectType, Schema

from recipes.schema import Mutation as RecipesMutation
from recipes.schema import Query as RecipesQuery


class Query(RecipesQuery, ObjectType):
    pass


class Mutation(RecipesMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
