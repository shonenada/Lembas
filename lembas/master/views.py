# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json

from flask import Blueprint, request, url_for, abort, Response

from lembas.store import current_store


bp = Blueprint('master', __name__)


@bp.route('/<key>')
def get_key(key):
    value = current_store.get(key)
    if value is None:
        return abort(404)
    data = json.dumps(value)
    return Response(data, mimetype='application/json')


@bp.route('/_/<key>', methods=['POST', 'PUT', 'PATCH'])
def set_key(key):
    data = request.get_json()
    if data is None:
        return abort(400)
    current_store.set(key, data)
    return url_for('master.get_key', key=key, _external=True)