# -*- coding: utf-8 -*-
from __future__ import absolute_import

import leancloud


class KV(leancloud.Object):

    @classmethod
    def create(cls, key, data):
        obj = cls()
        obj.set('key', key)
        obj.set('data', data)
        obj.save()
        return obj


class LeanCloudStore(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ak = app.config['STORE_LEANCLOUD_AK']
        sk = app.config['STORE_LEANCLOUD_SK']
        leancloud.init(ak, sk)

    def get(self, key):
        query = KV.query
        query.equal_to('key', key)
        obj = query.first()
        if obj is not None:
            return obj.get('data')
        return None

    def set(self, key, value):
        return KV.create(key, value)

    def remove(self, key):
        obj = self.get(key)
        obj.destroy()
        return True
