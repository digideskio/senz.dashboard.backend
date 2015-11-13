# coding: utf-8

from flask import session, request, redirect, url_for, make_response
from os.path import dirname, join
import json

from application import make_app
app = make_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        session['app_id'] = app_id
        return make_response(app_id)
    if request.method == 'GET':
        return redirect(url_for('dashboard_bp.show'))


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

