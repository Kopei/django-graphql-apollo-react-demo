# -*- coding:utf-8 -*-
import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id
import json
import status

from . import models


class MessageType(DjangoObjectType):
    class Meta:
        model = models.Message
        interfaces = (graphene.Node, )


class Query(object):
    all_messages = graphene.List(MessageType)

    def resolve_all_messages(self, info):
        return models.Message.objects.all()

    message = graphene.Field(MessageType, id=graphene.ID())

    def resolve_message(self, info, id):
        rid = from_global_id(id)
        # rid is a tuple: ('MessageType', '1')
        return models.Message.objects.get(pk=rid[1])


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        message = graphene.String()

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MessageType)

    def mutate(self, info, message):
        print('info context is %s' %dir(info.context))
        print('if auth', info.context.user.is_authenticated)
        if not info.context.user.is_authenticated:
            return CreateMessageMutation(status=status.HTTP_403_FORBIDDEN)
        message = message.get('message', '').strip()
        # Here we would usually use Django forms to validate the input
        if not message:
            return CreateMessageMutation(
                status=status.HTTP_400_BAD_REQUEST,
                formErrors=json.dumps(
                    {'message': ['Please enter a message.']}))
        obj = models.Message.objects.create(
            user=info.context.user, message=message
        )
        return CreateMessageMutation(status=status.HTTP_200_OK, message=obj)


class Mutation(object):
    create_message = CreateMessageMutation.Field()