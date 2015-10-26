# coding: utf-8

from flask import Blueprint, session, render_template, request, redirect, url_for
from leancloud import User
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
    user = User()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user.login(username, password)
        session['username'] = username
        session['session_token'] = user.get_session_token()
        return redirect('/')
    return render_template('login/login.html')


@login_view.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('session_token'):
        session['session_token'] = None
    if session.get('username'):
        session['username'] = None
    return redirect('/')


@login_view.route('/signup')
def signup():
    username = session.get('username')
    if username:
        return redirect(url_for('dashboard.show'), username=username)
