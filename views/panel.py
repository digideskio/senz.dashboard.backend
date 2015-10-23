import requests
from models import Developer
from flask import Blueprint, render_template, request

panel = Blueprint('panel', __name__, template_folder='templates')


@panel.route('/panel', methods=['GET', 'POST'])
def show():
    app_id = 'demo55bc5d8e00b0cb9c40dec37b'
    developer = Developer()
    developer.get_tracker_of_app(app_id)
    motion_dict = {'motionSitting': 0, 'motionWalking': 3, 'motionRunning': 4, 'motionBiking': 2, 'motionCommuting': 1}
    context_list = ['contextAtHome', 'contextCommutingWork', 'contextAtWork', 'contextCommutingHome',
                    'contextWorkingInCBD', 'contextStudyingInSchool', 'contextWorkingInSchool',
                    'contextOutdoorExercise', 'contextIndoorExercise', 'contextDinningOut', 'contextTravelling',
                    'contextShortTrip', 'contextInParty', 'contextWindowShopping', 'contextAtCinema',
                    'contextAtExhibition', 'contextAtPopsConcert', 'contextAtTheatre', 'contextAtClassicsConcert']

    if request.method == 'POST':
        type = request.form.get('type')
        val = request.form.get('val')
        if type and val:
            print type, val
            # if user.get_tracker_of_app(app_id):
            #     tracker_list = user.tracker_list
            headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
                       "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}
            payload = {"userId": "559b8bd5e4b0d4d1b1d35e88", "type": type, "val": val}
            # for tracker in tracker_list:
            requests.post("https://leancloud.cn/1.1/functions/notify_new_details",  headers=headers, data=payload)
            # requests.post("http://localhost:3000/functions/notify_new_details",  headers=headers, data=payload)
    return render_template('panel/panel.html',
                           motion_dict=motion_dict,
                           context_list=context_list,
                           tracker_list=developer.tracker_list)

