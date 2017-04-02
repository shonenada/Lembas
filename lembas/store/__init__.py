# -*- coding: utf-8 -*-
from __future__ import absolute_import

from werkzeug.local import LocalProxy
from flask import current_app, has_request_context

from lembas.store.memory import MemoryStore
from lembas.store.redis import RedisStore


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

        if app.config['STORE_BROKER'] == 'memory':
            self._broker = MemoryStore(app)

        if app.config['STORE_BROKER'] == 'redis':
            self._broker = RedisStore(app)


current_store = LocalProxy(lambda: _get_current_store())


def _get_current_store():
    if has_request_context():
        if current_app.extensions.get('store', None) is not None:
            store = current_app.extensions['store']
            return store.get_broker()
