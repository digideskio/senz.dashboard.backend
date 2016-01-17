from ..models import Developer
from os.path import dirname, join
from leancloud import Object
from application.common.util import post_panel_data
from flask import Blueprint, render_template, request, session, redirect, url_for, json

panel = Blueprint('panel', __name__, template_folder='templates')

Installation = Object.extend('BindingInstallation')


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

    s = json.load(file(join(dirname(dirname(__file__)), 'translate.json')))
    home_office_type = s.get("home_office_status").keys() + s.get("home_office_status_old").keys()

    if request.method == 'POST':
        tracker = request.form.get('tracker')
        motion_type = request.form.get('motionType')
        motion_val = request.form.get('motionVal')
        context_type = request.form.get('contextType')
        context_val = request.form.get('contextVal')
        source = request.form.get('source')
        if motion_type and motion_val:
            post_panel_data(tracker=tracker, tracker_list=tracker_list,
                            type="motion", value=motion_val, source=source)
        if context_type and context_val and context_type in home_office_type:
            post_panel_data(tracker=tracker, tracker_list=tracker_list,
                            type="home_office_status", value=context_val, source=source)
        if context_type and context_val and context_type not in home_office_type:
            post_panel_data(tracker=tracker, tracker_list=tracker_list,
                            type="event", value=context_val, source=source)

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


