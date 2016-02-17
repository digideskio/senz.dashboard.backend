# coding: utf-8
from flask import render_template, Blueprint, request, session, redirect, url_for, make_response
from application.models import Developer
from application.common.util import post_data
import json

exhibition_push = Blueprint('exhibition_push', __name__, template_folder='templates')


@exhibition_push.route('/dashboard/push')
def show():
    if not session.get('session_token'):
        next_url = '/dashboard/push'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    user_id = developer.user_id()
    app_list = developer.get_app_list()
    tracker_list = developer.get_tracker_of_app(app_id)
    if request.method == "POST":
        data = request.json
        data['devId'] = user_id
        data['appId'] = app_id
        url = "http://api.trysenz.com/notifyStrategy/createStrategy"
        rep = post_data(url=url, data=data)
        return make_response(json.dumps(rep))
    return render_template("dashboard/push-notification.html", username=username,
                           app_id=app_id, app_list=app_list, tracker_list=tracker_list)


@exhibition_push.route('/dashboard/history')
def history():
    if not session.get('session_token'):
        next_url = '/dashboard/push'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)
    if request.method == "POST":
        print request.json
    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()
    tracker_list = developer.get_tracker_of_app(app_id)
    return render_template('dashboard/push-notification-history.html', username=username,
                           app_id=app_id, app_list=app_list, tracker_list=tracker_list)