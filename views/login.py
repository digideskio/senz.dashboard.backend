# coding: utf-8

from flask import Blueprint, session, render_template, request, redirect, url_for
from leancloud import LeanCloudError
from models import Developer
import datetime

login_view = Blueprint('login_view', __name__, template_folder='templates')


def get_expiration():
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=30)
    return expire_date


@login_view.route('/login', methods=['GET', 'POST'])
def login():
    session_token = session.get('session_token')
    if session_token:
        return redirect('/')
    if request.method == 'POST':
        user = Developer()
        username = request.form['username']
        password = request.form['password']
        try:
            user.login(username, password)
            session['username'] = username
            session['user_id'] = user.id
            session['session_token'] = user.get_session_token()
        except LeanCloudError:
            return render_template('login/login.html')

        return redirect('/')
    return render_template('login/login.html')


@login_view.route('/logout', methods=['GET', 'POST'])
def logout():
    developer = Developer()
    developer.session_token = session.get('session_token')
    developer.logout()
    if session.get('session_token'):
        session['session_token'] = None
    if session.get('username'):
        session['username'] = None
    session.pop('app_list', None)
    session.pop('app_list', None)
    session.pop('app_list', None)
    return redirect('/')


@login_view.route('/signup', methods=['GET', 'POST'])
def signup():
    username = session.get('username')
    if username:
        return redirect(url_for('dashboard.show'), username)
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
            return redirect(url_for('login_view.login'))
        except LeanCloudError, e:
            print(e)
            return render_template('login/signup.html')
    return render_template('login/signup.html')
