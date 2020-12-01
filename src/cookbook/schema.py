from graphene import ObjectType, Schema

from recipes.graphql import Mutation as RecipesMutation
from recipes.graphql import Query as RecipesQuery
from recipes.graphql import Subscription as RecipesSubscription

from .graphql import Mutation as JWTMutation


class Query(RecipesQuery, ObjectType):
    pass


class Mutation(JWTMutation, RecipesMutation, ObjectType):
    pass


class Subscription(RecipesSubscription, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
