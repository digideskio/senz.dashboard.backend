# -*- coding:utf-8 -*-
from os.path import dirname, abspath
from datetime import timedelta


class Config(object):
    """配置基类"""
    # Flask app config
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    permanent_session_lifetime = timedelta(hours=1)

    # Root path of project
    PROJECT_PATH = abspath(dirname(dirname(__file__)))
