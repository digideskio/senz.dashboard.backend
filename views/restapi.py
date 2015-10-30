from flask import Blueprint, render_template, request, session, jsonify, url_for, abort
from flask.ext.httpauth import HTTPBasicAuth
from models import Developer

auth = HTTPBasicAuth()

restapi = Blueprint('restapi', __name__, template_folder='templates')


@restapi.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None:
        abort(400)
    user = Developer()
    user.set('email', email)
    user.set('username', username)
    user.set('password', password)
    user.set('type', 'developer')
    user.sign_up()
    # return jsonify({'username': user.username }), 201,
    # {'Location': url_for('get_user', id = user.id, _external = True)}
    return jsonify({'username': username}), 201


@restapi.route('/api/test')
@auth.login_required
def test():
    return jsonify({'data': 'Hello, REST!'})