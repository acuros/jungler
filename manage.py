#-*- coding: utf-8 -*-
from flask.ext.script import Manager

from jungler.app import create_app
from jungler.ext import db
from jungler.models import *

app = create_app()
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(globals(), **locals())


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000)


@manager.command
def initdb():
    print "* Creating database...",
    db.create_all(app=app)
    print "Done"


@manager.command
def dropdb():
    print "* Dropping database...",
    db.drop_all(app=app)
    print "Done"


@manager.command
def resetdb():
    dropdb()
    initdb()


if __name__ == '__main__':
    manager.run()