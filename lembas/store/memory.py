# -*- coding: utf-8 -*-
from __future__ import absolute_import


class MemoryStore(object):

    def __init__(self, app=None):
        self._data = {}

    def get(self, key):
        return self._data.get(key, None)

    def set(self, key, value):
        self._data[key] = value
        return value

    def remove(self, key):
        if key in self._data:
            del self._data[key]
            return True
        return False
