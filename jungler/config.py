#-*- coding: utf-8 -*-
"""
    jungler.config
    ~~~~~~~~~~~~~~

    This module provides configurations. Secret data is stored in `secret` module.

    :secret.DATABASE_PASSWORD: A password for database.
    :secret.SECRET_KEY: A secret key.
    :secret.RABBITMQ_PASSWORD: A password for rabbitmq.

"""
import os

from jungler import secret


class DefaultConfig(object):
    DEBUG = True
    TESTING = False

    SECRET_KEY = secret.SECRET_KEY

    BASE_DIR = BASE_DIR = os.path.dirname(__file__)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/jungler.db' % BASE_DIR
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = False

    NAVER_SEARCH_API_KEY = 'fc5ad3706cf041be6ec2b8fd2dda353b'
    BROKER_URL = "amqp://jungler:%s@localhost:5672/jungler" % (
        secret.RABBITMQ_PASSWORD
    )


class TestConfig(DefaultConfig):
    TESTING = True


class DeployConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
    SERVER_NAME = ''

    SQLALCHEMY_DATABASE_URI = 'mysql://jungler:%s@localhost/jungler' % secret.DATABASE_PASSWORD
    SQLALCHEMY_MAX_OVERFLOW = 16