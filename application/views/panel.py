import time
import requests
from ..models import Developer
from os.path import dirname, join
from flask import Blueprint, render_template, request, session, redirect, url_for, json

panel = Blueprint('panel', __name__, template_folder='templates')


@panel.route('/panel/debug', methods=['GET', 'POST'])
def show():
    if not session.get('session_token'):
        next_url = '/panel/debug'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()
    tracker_list = developer.get_tracker_of_app(app_id)

    if request.method == 'POST':
        tracker = request.form.get('tracker')
        motion_type = request.form.get('motionType')
        motion_val = request.form.get('motionVal')
        context_type = request.form.get('contextType')
        context_val = request.form.get('contextVal')
        source = request.form.get('source')
        post_panel_data(tracker=tracker,
                        tracker_list=tracker_list,
                        motion_type=motion_type,
                        motion_val=motion_val,
                        context_type=context_type,
                        context_val=context_val,
                        source=source)
    motion_list = ['motionSitting', 'motionWalking', 'motionRunning', 'motionBiking', 'motionCommuting']
    f = file(join(dirname(dirname(__file__)), 'translate.json'))
    context_list = filter(lambda x: str(x) != '', json.load(f).get('context').keys())
    return render_template('panel/debug.html',
                           username=username,
                           motion_list=motion_list,
                           context_list=context_list,
                           tracker_list=tracker_list,
                           app_id=app_id,
                           app_list=app_list)


def post_panel_data(**param):
    tracker = param.get('tracker')
    tracker_list = param.get('tracker_list')
    motion_type = param.get('motion_type')
    motion_val = param.get('motion_val')
    context_type = param.get('context_type')
    context_val = param.get('context_val')
    source = param.get('source')
    timestamp = param.get('timestamp') or int(time.time()*1000)

    # home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']

    s = json.load(file(join(dirname(dirname(__file__)), 'translate.json')))
    home_office_type = s.get("home_office_status").keys() + s.get("home_office_status_old").keys()

    if tracker != 'all':
        tracker_list = [tracker]
    headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
               "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}
    for item in tracker_list:
        payload = {"userId": item, "source": source, "timestamp": timestamp}
        if motion_type and motion_val:
            payload["type"] = motion_type
            payload["val"] = motion_val
            requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)
        if context_type and context_val and context_val in home_office_type:
            payload["type"] = "home_office_status"
            payload["val"] = context_val
            requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)
        elif context_type and context_val and context_val not in home_office_type:
            payload["type"] = "event"
            payload["val"] = context_val
            requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)

