# coding: utf-8

from flask import Flask, session, request, redirect, url_for, make_response
from datetime import timedelta
from config import load_config
from application.views.panel import panel
from application.views.integration import integration
from application.views.settings import settings
from application.views.account import accounts_bp
from application.views.exhibition.index import exhibition_index
from application.views.exhibition.profile import exhibition_profile
from application.views.exhibition.interest import exhibition_interest
from application.views.exhibition.consumption import exhibition_consumption
from application.views.exhibition.marriage import exhibition_marriage
from application.views.exhibition.location import exhibition_location
from application.views.exhibition.context import exhibition_context
from application.views.exhibition.single_user import exhibition_single
from application.views.exhibition.group import exhibition_group
from application.views.exhibition.push import exhibition_push
from os.path import dirname, join
import bugsnag
from bugsnag.flask import handle_exceptions
import json

bugsnag.configure(
    api_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT",
    project_root=dirname(dirname(__file__)),
)

app = Flask(__name__)
config = load_config()
handle_exceptions(app)
app.config.from_object(config)
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(panel)
app.register_blueprint(exhibition_index)
app.register_blueprint(exhibition_profile)
app.register_blueprint(exhibition_interest)
app.register_blueprint(exhibition_consumption)
app.register_blueprint(exhibition_marriage)
app.register_blueprint(exhibition_location)
app.register_blueprint(exhibition_context)
app.register_blueprint(exhibition_single)
app.register_blueprint(exhibition_group)
app.register_blueprint(exhibition_push)
app.register_blueprint(integration)
app.register_blueprint(settings)
app.register_blueprint(accounts_bp)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        session['app_id'] = app_id
        return make_response(app_id)
    if request.method == 'GET':
        return redirect(url_for('exhibition_index.show'))


@app.template_filter('translate')
def translate(target, arg):
    f = file(join(dirname(__file__), 'translate.json'))
    s = json.load(f)
    if arg == 'motion':
        return s.get('motion').get(target)
    elif arg == 'interest':
        return s.get('interest').get(target)
    elif arg == 'context':
        return s.get('context').get(target)
    else:
        return ''

