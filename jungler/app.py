#-*- coding: utf-8 -*-
from flask import Flask

from jungler.config import DefaultConfig


def hello():
    from math import ceil
    line_length = 80
    msg = 'Jungler'
    left = (line_length - len(msg)) / 2 - 3
    right = int(ceil((line_length - len(msg)) / 2.0) - 3)
    line = '#' * line_length
    print line
    print '#', ' ' * left, msg, ' ' * right, '#'
    print line


def create_app(config=DefaultConfig(), verbose=False):
    if verbose:
        hello()

    app = Flask(__name__)
    app.config.from_object(config)
    init_ext(app)
    init_log(app)
    return app


def init_ext(app):
    from jungler.ext import init_db, init_assets
    init_db(app)
    init_assets(app)


def init_log(app):
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    import logging
    logging.basicConfig(filename='logs/db.log')
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('logs/request.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)