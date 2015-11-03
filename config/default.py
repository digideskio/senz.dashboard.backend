# -*- coding:utf-8 -*-
from os.path import dirname, abspath


class Config(object):
    """配置基类"""
    # Flask app config
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    # Root path of project
    PROJECT_PATH = abspath(dirname(dirname(__file__)))
