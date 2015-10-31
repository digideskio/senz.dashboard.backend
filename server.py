# coding: utf-8

from flask import Flask, session, request, redirect
from itsdangerous import Signer
from views.panel import panel
from views.restapi import restapi
from views.dashboard import dashboard_bp
from views.integration import integration
from views.settings import settings
from views.account import accounts_bp
from datetime import timedelta
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
signer = Signer(app.config['SECRET_KEY'])
app.permanent_session_lifetime = timedelta(hours=1)

cache = SimpleCache()

# 动态路由
app.register_blueprint(panel)
app.register_blueprint(dashboard_bp)
app.register_blueprint(integration)
app.register_blueprint(settings)
app.register_blueprint(accounts_bp)
app.register_blueprint(restapi)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        session['app_id'] = app_id
        return redirect('/')
    if request.method == 'GET':
        return redirect('/dashboard')


@app.template_filter('translate_motion')
def translate_motion(s):
    library = {'motionCommuting': '乘车',   'motionWalking': '走路', 'motionSitting': '静坐',
               'motionBiking': '骑车', 'motionRunning': '跑步', '': ''}
    return library[s]


@app.template_filter('translate_interest')
def translate_interest(s):
    library = {"jogging": "慢跑", "fitness": "健身", "basketball": "篮球", "football": "足球", "badminton": "羽毛球",
               "bicycling": " 骑车", "table_tennis": "网球", 'social': "社交", 'online_shopping': "网络购物",
               'offline_shoppng': "线下购物", 'tech_news': "教育新闻", 'entertainment_news': "娱乐新闻", 'current_news': "时事新闻",
               'business_news': "商业新闻", 'sports_news': "运动新闻",  'game_news': "游戏新闻", 'study': "学霸", 'gamer': "游戏玩家",
               'health': "健康", 'sports_show': "体育节目", 'game_show': "游戏节目", "variety_show": "综艺节目",
               'tvseries_show': "电视剧", 'acg': "动漫", 'indoorsman': "宅男", '': ''}
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
               'contextAtClassicsConcert': '音乐会', '': ''}
    return library[s]


