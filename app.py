# coding: utf-8

from datetime import datetime

from flask import Flask
from flask import render_template
from views.panel import panel
from views.dashboard import dashboard
from views.dash_source import dash_source
from views.integration import integration
from views.settings import settings

app = Flask(__name__)

# 动态路由
app.register_blueprint(panel)
app.register_blueprint(dashboard)
app.register_blueprint(dash_source)
app.register_blueprint(integration)
app.register_blueprint(settings)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())
