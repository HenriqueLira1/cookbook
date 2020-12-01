from graphene import ObjectType, Schema

from recipes.schema import Mutation as RecipesMutation
from recipes.schema import Query as RecipesQuery
from recipes.schema import Subscription as RecipesSubscription


class Query(RecipesQuery, ObjectType):
    pass


class Mutation(RecipesMutation, ObjectType):
    pass


class Subscription(RecipesSubscription, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
