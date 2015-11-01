# coding: utf-8

from flask import Blueprint, session, render_template, request, redirect, url_for
from leancloud import LeanCloudError
from models import Developer
import datetime
import server

accounts_bp = Blueprint('accounts_bp', __name__, template_folder='templates')


def get_expiration():
    return datetime.datetime.now() + datetime.timedelta(days=30)


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('session_token'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = Developer()
        print(user.get_session_token())
        username = request.form['username']
        password = request.form['password']
        try:
            user.login(username, password)
            session['session_token'] = user.get_session_token()
        except LeanCloudError:
            return render_template('account/login.html')
        return redirect(url_for('index'))
    return render_template('account/login.html')


@accounts_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    developer = Developer()
    developer.session_token = session.get('session_token')
    developer.logout()
    session.clear()
    server.cache.clear()
    return redirect(url_for('index'))


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
