from flask import Blueprint, request, jsonify, make_response, abort, g
from flask.ext.httpauth import HTTPBasicAuth
from leancloud import LeanCloudError
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
    return jsonify({'username': username}), 201


@restapi.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@restapi.route('/api/test')
@auth.login_required
def test():
    return jsonify({'data': 'Hello,  test!'})


@auth.verify_password
def verify_token(username_or_token, password):
    user = Developer.verify_auth_token(username_or_token)
    if not user:
        user = Developer()
        try:
            user.login(username_or_token, password)
            if user.get_session_token():
                g.user = user
                user.logout()
                return True
        except LeanCloudError:
            g.user = None
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
