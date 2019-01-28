# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django import mixer
from graphql_relay import to_global_id
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from unittest import mock
from .. import schema


pytestmark = pytest.mark.django_db


class NewRequestFactory(RequestFactory):
    def __init__(self, *args, **defaults):
        self.context = mock.Mock()
        self.set_user()
        super().__init__(*args, **defaults)

    def set_user(self):
        setattr(self.context, 'user', '')


def test_message_type():
    instance = schema.MessageType()
    assert instance


def test_resolve_all_messages():
    mixer.blend('simple_app.Message')
    mixer.blend('simple_app.Message')
    q = schema.Query()
    res = q.resolve_all_messages(None)
    assert res.count() == 2, 'Should return all messages'


def test_resolve_message():
    msg = mixer.blend('simple_app.Message')
    q = schema.Query()
    id = to_global_id('MessageType', msg.pk)
    res = q.resolve_message(None, id)
    assert res == msg, 'Should return the requested message'


def test_create_message_mutation():
    user = mixer.blend('auth.User')
    mut = schema.CreateMessageMutation()

    data = {'message': 'Test'}
    req = NewRequestFactory()
    req.context.user = AnonymousUser()
    res = mut.mutate(req, data)
    assert res.status == 403, 'Should return 403 if user is not logged in'

    req.context.user = user
    res = mut.mutate(req, {})
    assert res.status == 400, 'Should return 400 if there are form errors'
    assert 'message' in res.formErrors, (
        'Should have form error for message field')

    res = mut.mutate(req, data)
    assert res.status == 200, 'Should return 200 if mutation is successful'
    assert res.message.pk == 1, 'Should create new message'