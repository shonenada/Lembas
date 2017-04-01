# -*- coding: utf-8 -*-
from __future__ import absolute_import


class MemoryStore(object):

    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(key, None)

    def set(self, key, value):
        self._data[key] = value
        return value
