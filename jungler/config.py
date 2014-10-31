#-*- coding: utf-8 -*-
"""
    jungler.config
    ~~~~~~~~~~~~~~

    This module provides configurations. Secret data is stored in `secret` module.

    :secret.DATABASE_PASSWORD: A password for database.
    :secret.SECRET_KEY: A secret key.
"""
import os

from jungler import secret


class DefaultConfig(object):
    DEBUG = True
    TESTING = True

    SECRET_KEY = secret.SECRET_KEY

    BASE_DIR = BASE_DIR = os.path.dirname(__file__)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/jungler.db' % BASE_DIR
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = False
    #SQLALCHEMY_POOL_SIZE = 64
    #SQLALCHEMY_MAX_OVERFLOW = 16

    NAVER_SEARCH_API_KEY = 'fc5ad3706cf041be6ec2b8fd2dda353b'


class TestConfig(DefaultConfig):
    pass


class DeployConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
    SERVER_NAME = ''