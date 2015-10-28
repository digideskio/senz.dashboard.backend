from flask import Blueprint, render_template, session, request, redirect, jsonify
from models import Developer

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/settings')
def show():
    app_id = session.get('app_id')
    app_key = session.get('app_key')
    user = Developer()
    user.session_token = session.get('session_token')
    # user_id = user.user_id()
    user.get_app_list()
    return render_template('settings/settings.html',
                           username=session.get('username'),
                           app_id=app_id, app_key=app_key,
                           app_list=user.app_list)


@settings.route('/delete', methods=['GET', 'POST'])
def delete_app():
    app_id = request.form.get('app_id')
    user = Developer()
    user.session_token = session.get('session_token')
    if user.delete_app(app_id):
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
            return jsonify({'delete': 'success'})
        else:
            return jsonify({'delete': 'failed'})
