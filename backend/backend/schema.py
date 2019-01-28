import graphene
from simple_app import schema


class Queries(schema.Query, graphene.ObjectType):
    dummy = graphene.String()


class Mutations(schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)