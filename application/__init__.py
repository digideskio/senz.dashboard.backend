# coding: utf-8

from flask import Flask
from datetime import timedelta
from config import load_config
from application.views.panel import panel
from application.views.dashboard import dashboard_bp
from application.views.integration import integration
from application.views.settings import settings
from application.views.account import accounts_bp
from os.path import dirname
import bugsnag
from bugsnag.flask import handle_exceptions


bugsnag.configure(
    api_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT",
    project_root=dirname(dirname(__file__)),
)


def make_app():
    app = Flask(__name__)
    config = load_config()
    handle_exceptions(app)
    app.config.from_object(config)
    app.permanent_session_lifetime = timedelta(hours=1)
    register_routes(app, panel, dashboard_bp, integration,
                    settings, accounts_bp)
    return app


def register_routes(app, *route_list):
    for route in route_list:
        app.register_blueprint(route)
