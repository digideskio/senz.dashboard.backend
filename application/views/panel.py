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


