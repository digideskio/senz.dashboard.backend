# coding: utf-8

from flask import Flask, session
from flask import render_template
from views.panel import panel
from views.dashboard import dashboard
from views.dash_source import dash_source
from views.integration import integration
from views.settings import settings
from views.login import login_view

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is senz dashboard'

# 动态路由
app.register_blueprint(panel)
app.register_blueprint(dashboard)
app.register_blueprint(dash_source)
app.register_blueprint(integration)
app.register_blueprint(settings)
app.register_blueprint(login_view)


@app.route('/')
def index():
    username = session.get('username')
    print(username)
    return render_template('index.html', username=username)


@app.template_filter('translate_motion')
def translate_motion(s):
    library = {'motionCommuting': '乘车',   'motionWalking': '走路', 'motionSitting': '静坐',
               'motionBiking': '骑车', 'motionRunning': '跑步'}
    return library[s]


@app.template_filter('translate_context')
def translate_context(s):
    library = {'contextAtHome': '在家', 'contextCommutingWork': '上班路上', 'contextAtWork': '在公司',
               'contextCommutingHome': '回家路上', 'contextWorkingInCBD': '商圈工作中',
               'contextStudyingInSchool': '学校上课中', 'contextWorkingInSchool': '学校工作中',
               'contextOutdoorExercise': '户外锻炼', 'contextIndoorExercise': '室内锻炼',
               'contextDinningOut': '在餐厅吃饭', 'contextTravelling': '旅游', 'contextShortTrip': '郊游',
               'contextInParty': '聚会', 'contextWindowShopping': '逛街', 'contextAtCinema': '看电影',
               'contextAtExhibition': '展览会', 'contextAtPopsConcert': '演唱会', 'contextAtTheatre': '戏剧',
               'contextAtClassicsConcert': '音乐会'}
    return library[s]
