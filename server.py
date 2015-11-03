# coding: utf-8

from flask import Flask, session, request, redirect, url_for
from itsdangerous import Signer
from views.panel import panel
from views.restapi import restapi
from views.dashboard import dashboard_bp
from views.integration import integration
from views.settings import settings
from views.account import accounts_bp
from datetime import timedelta
from werkzeug.contrib.cache import SimpleCache
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
signer = Signer(app.config['SECRET_KEY'])
app.permanent_session_lifetime = timedelta(hours=1)

cache = SimpleCache()


# 动态路由
app.register_blueprint(panel)
app.register_blueprint(dashboard_bp)
app.register_blueprint(integration)
app.register_blueprint(settings)
app.register_blueprint(accounts_bp)
app.register_blueprint(restapi)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        session['app_id'] = app_id
        cache.clear()
        return redirect(url_for('dashboard_bp.show'))
    if request.method == 'GET':
        return redirect(url_for('dashboard_bp.show'))


@app.template_filter('translate')
def translate(target, arg):
    f = file("translate.json")
    s = json.load(f)
    if arg == 'motion':
        return s.get('motion').get(target)
    elif arg == 'interest':
        return s.get('interest').get(target)
    elif arg == 'context':
        return s.get('context').get(target)
    else:
        return ''

