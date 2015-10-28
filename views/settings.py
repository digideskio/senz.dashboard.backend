from flask import Blueprint, render_template, session, request, jsonify
from models import Developer

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/settings')
def show():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    return render_template('settings/settings.html',
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


@settings.route('/delete', methods=['GET', 'POST'])
def delete_app():
    app_id = request.form.get('app_id')
    user = Developer()
    user.session_token = session.get('session_token')
    if user.delete_app(app_id):
        session.pop('app_list', None)
        return jsonify({'delete': 'success'})
    else:
        return jsonify({'delete': 'failed'})


@settings.route('/create', methods=['POST'])
def add_app():
    if request.method == 'POST':
        app_name = request.form['app_name']
        user = Developer()
        user.session_token = session.get('session_token')
        if user.create_new_app(app_name):
            session.pop('app_list', None)
            return jsonify({'delete': 'success'})
        else:
            return jsonify({'delete': 'failed'})
