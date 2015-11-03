# coding: utf-8
from .default import Config


class TestingConfig(Config):
    # App config
    TESTING = True

    # Disable csrf while testing
    WTF_CSRF_ENABLED = False

    # Db config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db_test.sqlite3'
