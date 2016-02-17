# coding: utf-8
from flask import render_template, Blueprint, request, session
from common import get_app_list, get_tracker_of_app, get_attr_of_user
from application.models import Developer
import json

exhibition_single = Blueprint('exhibition_single', __name__, template_folder='templates')


@exhibition_single.route('/dashboard/single', methods=['GET', 'POST'])
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    developer = Developer()
    developer.session_token = session.get('session_token')
    if request.method == 'POST':
        req_type = request.json.get('type')
        group_id = request.json.get('gourpid')

        if req_type == 'user_list':
            return json.dumps({"userNames": get_tracker_of_app(app_id, group_id=group_id)})

        uid = request.json.get('uid')
        h_start = request.json.get('h_start')
        h_end = request.json.get('h_end')
        e_start = request.json.get('e_start')
        e_end = request.json.get('e_end')
        workday = request.json.get('workday')
        ret_dict = get_attr_of_user(uid, h_start=h_start, h_end=h_end,
                                    e_start=e_start, e_end=e_end, workday=workday == 'workday')
        return json.dumps(ret_dict)
    return render_template('dashboard/single-user-motion.html',
                           username=username, app_id=app_id, app_list=app_list)