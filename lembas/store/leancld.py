# -*- coding: utf-8 -*-
from __future__ import absolute_import

import leancloud
from leancloud import LeanCloudError


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

    def get_obj(self, key):
        query = KV.query
        query.equal_to('key', key)
        try:
            obj = query.first()
        except LeanCloudError:
            return None
        return obj

    def get(self, key):
        obj = self.get_obj(key)
        if obj is not None:
            return obj.get('data')
        return None

    def set(self, key, value):
        obj = self.get_obj(key)
        if obj is not None:
            obj.set('data', value)
            obj.save()
            return obj
        return KV.create(key, value)

    def remove(self, key):
        obj = self.get_obj(key)
        if obj is None:
            return False
        obj.destroy()
        return True
