# -*- coding: utf-8

from __future__ import absolute_import

from werkzeug.utils import import_string
from flask import Flask, current_app, request, session
from envcfg.raw import lembas

from lembas.utils.logger import setup_logger


blueprints = [
    'lembas.master.views:bp',
]


def create_app(name=None, config=None):
    app = Flask(name or __name__)

    app.config.from_object('envcfg.raw.lembas')

    app.debug = bool(int(lembas.DEBUG))
    app.config['TESTING'] = bool(int(lembas.TESTING))

    setup_logger(app)
    setup_hook(app)

    for bp_import_name in blueprints:
        bp = import_string(bp_import_name)
        app.register_blueprint(bp)

    return app


def setup_hook(app):
    app.after_request(_request_log)


def _request_log(resp, *args, **kwargs):
    current_app.logger.info(
        '{addr} request: [{status}] {method}, url: {url}'.format(
            addr=request.remote_addr,
            status=resp.status,
            method=request.method,
            url=request.url,))
    return resp
