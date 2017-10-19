# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Blueprint, request, url_for, abort, Response, jsonify, render_template_string

from lembas.store import current_store


bp = Blueprint('master', __name__)

mimes = {
    'txt': 'plain/text',
    'json': 'application/json',
    'svg': 'image/svg+xml',
}


@bp.route('/')
def index():
    return jsonify(
        host=url_for('master.index', _external=True))


@bp.route('/<key>.<ext>')
def get_key(key, ext):
    value = current_store.get(key)
    if value is None:
        return abort(404)
    mime = mimes.get(ext, 'plain/text')
    data = request.args.to_dict()
    tml = render_template_string(value, **data)
    return Response(value, mimetype=mime)


@bp.route('/_/<key>', methods=['POST', 'PUT', 'PATCH'])
def set_key(key):
    data = request.data
    if data is None:
        return abort(400)
    ext = request.args.get('ext', 'json')
    current_store.set(key, data)
    url = url_for('master.get_key', key=key, ext=ext, _external=True)
    return jsonify(success=True, url=url)


@bp.route('/_/<key>', methods=['DELETE'])
def delete_key(key):
    rv = current_store.remove(key)
    return jsonify(success=rv)
