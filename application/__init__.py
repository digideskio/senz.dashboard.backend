# coding: utf-8

from flask import Flask
from config import load_config
from .views.panel import panel
from .views.restapi import restapi
from .views.dashboard import dashboard_bp
from .views.integration import integration
from .views.settings import settings
from .views.account import accounts_bp


def make_app():
    app = Flask(__name__)
    config = load_config()
    app.config.from_object(config)
    register_routes(app, panel, restapi, dashboard_bp,
                    integration, settings, accounts_bp)
    return app


def register_routes(app, *route_list):
    for route in route_list:
        app.register_blueprint(route)
