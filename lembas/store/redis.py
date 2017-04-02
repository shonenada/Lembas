# -*- coding: utf-8 -*-
from __future__ import absolute_import

import redis


class RedisStore(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('STORE_REDIS_HOST', 'localhost')
        app.config.setdefault('STORE_REDIS_PORT', 6379)
        app.config.setdefault('STORE_REDIS_DB', 0)

        self._conn = redis.StrictRedis(
            host=app.config['STORE_REDIS_HOST'],
            port=int(app.config['STORE_REDIS_PORT']),
            db=int(app.config['STORE_REDIS_DB']),)

    def get(self, key):
        return self._conn.get(key)

    def set(self, key, value):
        self._conn.set(key, value)
        return value

    def remove(self, key):
        if self._conn.keys(key):
            self._conn.delete(key)
            return True
        return False
