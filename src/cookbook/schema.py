from graphene import ObjectType, Schema

from recipes.schema import Query as RecipesQuery


class Query(RecipesQuery, ObjectType):
    # This class will inherit from multiple Queries
    # as more apps are added to the project
    pass


schema = Schema(query=Query)
