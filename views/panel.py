import requests
from models import Developer
from flask import Blueprint, render_template, request, session, redirect, url_for
import server

panel = Blueprint('panel', __name__, template_folder='templates')


@panel.route('/panel/debug', methods=['GET', 'POST'])
def show():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = server.cache.get('app_list')
    tracker_list = server.cache.get('tracker_list')
    if not app_list:
        app_list = developer.get_app_list()
        server.cache.set('app_list', app_list)
    if not tracker_list:
        tracker_list = developer.get_tracker_of_app(app_id)
        print(tracker_list)
        server.cache.set('tracker_list', tracker_list)

    if request.method == 'POST':
        tracker = request.form.get('tracker')
        motion_type = request.form.get('motionType')
        motion_val = request.form.get('motionVal')
        context_type = request.form.get('contextType')
        context_val = request.form.get('contextVal')
        post_panel_data(tracker=tracker,
                        tracker_list=tracker_list,
                        motion_type=motion_type,
                        motion_val=motion_val,
                        context_type=context_type,
                        context_val=context_val)

    motion_dict = {'motionSitting': 0, 'motionWalking': 3, 'motionRunning': 4, 'motionBiking': 2, 'motionCommuting': 1}
    context_list = ['contextAtHome', 'contextCommutingWork', 'contextAtWork', 'contextCommutingHome',
                    'contextWorkingInCBD', 'contextStudyingInSchool', 'contextWorkingInSchool',
                    'contextOutdoorExercise', 'contextIndoorExercise', 'contextDinningOut', 'contextTravelling',
                    'contextShortTrip', 'contextInParty', 'contextWindowShopping', 'contextAtCinema',
                    'contextAtExhibition', 'contextAtPopsConcert', 'contextAtTheatre', 'contextAtClassicsConcert']
    return render_template('panel/debug.html',
                           username=username,
                           motion_dict=motion_dict,
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

    if tracker != 'all':
        tracker_list = [tracker]
    headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
               "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}
    for item in tracker_list:
        payload = {"userId": item, "type": motion_type, "val": motion_val}
        requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)
        payload = {"userId": item, "type": context_type, "val": context_val}
        requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)

