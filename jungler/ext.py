#-*- coding: utf-8 -*-
import os

from flask.ext.sqlalchemy import SQLAlchemy

from jungler.config import DefaultConfig as Config

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


def init_assets(app, verbose=False):
    from flask.ext.assets import Bundle, Environment

    def hook_assets(directory, excludes):
        path = os.path.join(app.static_folder, directory)
        files = []
        for f in os.listdir(path):
            if f[0] != '.' and f[0] != '_' and f not in excludes:
                files.append('%s/%s' % (directory, f))
                if verbose:
                    print '* %s' % f
        return files

    def filters(*args):
        if Config.DEBUG:  # do not apply minify filter in debug mode
            args = [arg for arg in args if arg[-3:] != 'min']
        filters_ = ','.join(args) or None
        return filters_

    assets = Environment(app)
    assets.register(
        'css_lib',
        'bower_components/bootstrap/dist/css/bootstrap.css',
        filters=filters('cssmin'),
        output='dist/lib.css'
    )

    assets.register(
        'js_lib',
        'bower_components/jquery/dist/jquery.js',
        'bower_components/bootstrap/dist/js/bootstrap.js',
        filters=filters('jsmin'),
        output='dist/lib.js'
    )
    if verbose:
        print '#' * 80
    return assets