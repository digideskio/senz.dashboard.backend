# coding: utf-8

from flask import Blueprint, session, render_template, request, redirect, url_for
from leancloud import LeanCloudError
from ..models import Developer
import datetime
import leancloud

accounts_bp = Blueprint('accounts_bp', __name__, template_folder='templates')


def get_expiration():
    return datetime.datetime.now() + datetime.timedelta(days=30)


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or url_for('index')
    print(next_url)
    if session.get('session_token'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = Developer()
        username = request.form['username']
        password = request.form['password']
        try:
            user.login(username, password)
            session['session_token'] = user.get_session_token()
        except LeanCloudError:
            return render_template('account/login.html')
        return redirect(next_url)
    return render_template('account/login.html')


@accounts_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    next_url = request.args.get('next') or url_for('index')
    developer = Developer()
    developer.session_token = session.get('session_token')
    session.clear()
    developer.logout()
    return redirect(next_url)


@accounts_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Developer()
        try:
            user.set('email', email)
            user.set('username', username)
            user.set('password', password)
            user.set('type', 'developer')
            user.sign_up()
            return redirect(url_for('accounts_bp.login'))
        except LeanCloudError, e:
            print(e)
            return render_template('account/signup.html')
    return render_template('account/signup.html')


@accounts_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('account/reset.html')
    user = Developer()
    if session.get('session_token'):
        user.session_token = session.get('session_token')
        user.logout()
    email = request.form['email_phone']
    print(email)
    user.request_password_reset(email=email)
    return render_template('account/notify.html')


@accounts_bp.route('/forget', methods=['GET'])
def forget():
    return render_template('account/forget.html')
