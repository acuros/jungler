#-*- coding: utf-8 -*-
from flask import Flask, redirect, url_for

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
    init_blueprints(app)

    @app.route("/")
    def index():
        return redirect(url_for('feed.feeds'))

    return app


def init_ext(app):
    from jungler.ext import init_db, init_assets, init_celery
    init_db(app)
    init_assets(app)
    init_celery(app)


def init_log(app):
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    import logging
    logging.basicConfig(filename='logs/db.log')
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def init_blueprints(app):
    from jungler.web.feed import blueprint as feed
    from jungler.web.keyword import blueprint as keyword
    app.register_blueprint(feed)
    app.register_blueprint(keyword)