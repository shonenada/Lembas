# -*- coding: utf-8 -*-
from __future__ import absolute_import

from werkzeug.local import LocalProxy
from flask import current_app, has_request_context

from lembas.store.memory import MemoryStore
from lembas.store.redis import RedisStore
from lembas.store.leancld import LeanCloudStore


class _StoreState(object):

    def __init__(self, store):
        self.store = store

    def get_broker(self):
        return self.store._broker


class StoreBackend(object):

    def __init__(self, app=None):
        self._broker = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('STORE_BROKER', 'memory')
        app.extensions['store'] = _StoreState(self)

        broker = app.config['STORE_BROKER']

        if broker == 'memory':
            self._broker = MemoryStore(app)

        if broker == 'redis':
            self._broker = RedisStore(app)

        if broker == 'leancloud':
            self._broker = LeanCloudStore(app)


current_store = LocalProxy(lambda: _get_current_store())


def _get_current_store():
    if has_request_context():
        if current_app.extensions.get('store', None) is not None:
            store = current_app.extensions['store']
            return store.get_broker()
