# coding: utf-8
from flask import Blueprint, render_template, json, session, redirect, url_for
from leancloud import Object, Query, LeanCloudError
from ..models import Developer

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates')


def get_app_list():
    ret_dict = {}
    app_id = session.get('app_id')
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    # app_list = server.cache.get('app_list')
    # if not app_list:
    app_list = developer.get_app_list()
    # server.cache.set('app_list', app_list)
    ret_dict['app_id'] = app_id
    ret_dict['username'] = username
    ret_dict['app_list'] = app_list
    return ret_dict


@dashboard_bp.route('/dashboard')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('event')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'event')
    # server.cache.set('event', result_dict, timeout=10*60)
    event_list = [] if 'event' not in result_dict else result_dict['event']
    event_list = map(lambda x: translate_context(x), event_list)
    event_tmp = sorted(map(lambda x: (x, event_list.count(x)), set(event_list)), key=lambda item: -item[1])
    data = map(lambda x: {'rank': x/3+1, 'name': event_tmp[x-1][0]}, xrange(1, len(set(event_tmp))+1))
    event = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('index.html',
                           username=username,
                           app_id=app_id,
                           app_list=app_list,
                           option=json.dumps(event))


@dashboard_bp.route('/dashboard/profile')
def profile():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('profile')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'gender', 'age', 'occupation', 'field')
    # server.cache.set('profile', result_dict, timeout=10*60)
    gender_list = [] if 'gender' not in result_dict else result_dict['gender']
    age_list = [] if 'age' not in result_dict else result_dict['age']
    occupation_list = [] if 'occupation' not in result_dict else result_dict['occupation']
    field_list = [] if 'field' not in result_dict else result_dict['field']

    gender = {'category': ['male', 'female'], 'series': [gender_list.count('male'), gender_list.count('female')]}
    age = {"category": ["55up", "35to55", "16to35", "16down"],
           "series": [age_list.count('55up'), age_list.count('35to55'),
                      age_list.count('16to35'), age_list.count('16down')]}
    occupation_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, occupation_list.count(x)], set(occupation_list))))
    occupation = {"category": occupation_tmp[0], "series": occupation_tmp[1]} if occupation_tmp else {}
    field_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, field_list.count(x)], set(field_list))))
    field = {"category": field_tmp[0], "series": field_tmp[1]} if field_tmp else {}

    data = {'gender': gender, 'age': age, 'job': occupation, 'profession': field}
    user_profile = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-identity.html',
                           option=json.dumps(user_profile),
                           username=username,
                           app_id=app_id,
                           app_list=app_list)


@dashboard_bp.route('/dashboard/interest')
def interest():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('interest')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'interest')
    # server.cache.set('interest', result_dict, timeout=10*60)
    interest_list = [] if 'interest' not in result_dict else result_dict['interest']
    interest_list = map(lambda x: translate_interest(x), interest_list)
    interest_tmp = sorted(map(lambda x: (x, interest_list.count(x)), set(interest_list)), key=lambda item: -item[1])
    if interest_tmp:
        data = map(lambda x: {'rank': x, 'name': interest_tmp[x-1][0]}, xrange(1, 9))
        data.append({'rank': 9, 'name': '...'})
    else:
        data = []
    interest = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-hobby.html',
                           option=json.dumps(interest),
                           username=username,
                           app_id=app_id,
                           app_list=app_list)


@dashboard_bp.route('/dashboard/marriage')
def marriage():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('marriage')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'marriage', 'pregnant')
    # server.cache.set('marriage', result_dict, timeout=10*60)
    marriage_list = [] if 'marriage' not in result_dict else result_dict['marriage']
    pregnant_list = [] if 'pregnant' not in result_dict else result_dict['pregnant']

    marriage = {'category': ['yes', 'no'], 'series': [marriage_list.count('yes'), marriage_list.count('no')]}
    pregnant = {'category': ['yes', 'no'], 'series': [pregnant_list.count('yes'), pregnant_list.count('no')]}
    ret_json = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'marriage': marriage,
            'pregnant': pregnant
        }
    }
    return render_template('dashboard/user-matrimony.html',
                           option=json.dumps(ret_json),
                           username=username,
                           app_id=app_id,
                           app_list=app_list)


@dashboard_bp.route('/dashboard/consumption')
def consumption():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('consumption')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'consumption', 'has_car', 'has_pet')
    # server.cache.set('consumption', result_dict, timeout=10*60)
    consumption_list = [] if 'consumption' not in result_dict else result_dict['consumption']
    car_list = [] if 'has_car' not in result_dict else result_dict['has_car']
    pet_list = [] if 'has_pet' not in result_dict else result_dict['has_pet']

    consumption_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, consumption_list.count(x)], set(consumption_list))))
    consumption = {"category": consumption_tmp[0],  "series": consumption_tmp[1]} if consumption_tmp else {}
    car = {'category': ['yes', 'no'], 'series': [car_list.count('yes'), car_list.count('no')]}
    pet = {'category': ['yes', 'no'], 'series': [pet_list.count('yes'), pet_list.count('no')]}

    ret_json = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'consumption': consumption,
            'car': car,
            'pet': pet
        }
    }
    return render_template('dashboard/user-consumption.html',
                           option=json.dumps(ret_json),
                           username=username,
                           app_id=app_id,
                           app_list=app_list)


@dashboard_bp.route('/dashboard/location')
def location():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    # result_dict = server.cache.get('location')
    # if not result_dict:
    result_dict = get_query_list(app_id, 'province', 'city')
    # server.cache.set('location', result_dict, timeout=10*60)
    provice_list = [] if 'province' not in result_dict else result_dict['province']
    city_list = [] if 'city' not in result_dict else result_dict['city']

    province = map(lambda x: {'name': x[0], 'value': x[1]},
                   sorted(map(lambda x: (x, provice_list.count(x)), set(provice_list)), key=lambda x: -x[1]))
    city = map(lambda x: {'name': x[0], 'value': x[1]},
               sorted(map(lambda x: (x, city_list.count(x)), set(city_list)), key=lambda x: -x[1]))
    location = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'province': province,
            'city': city
        }
    }
    return render_template('dashboard/user-location.html',
                           username=username,
                           app_id=app_id,
                           app_list=app_list,
                           option=json.dumps(location))


@dashboard_bp.route('/dashboard/context')
def motion():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']
    result_dict = get_query_list(app_id, 'home_office_status', 'event')

    home_office_list = [] if 'home_office_status' not in result_dict else result_dict['home_office_status']
    event_list = [] if 'event' not in result_dict else result_dict['event']

    event_list = map(lambda x: translate_context(x), filter(lambda x: x not in home_office_type, event_list))
    event_tmp = sorted(map(lambda x: (x, event_list.count(x)), set(event_list)), key=lambda item: -item[1])

    home_office_tmp = map(lambda x: map(lambda y: y[1], sorted(x.items(), key=lambda key: int(key[0][6:]))), home_office_list)
    series = map(lambda x: list(x), zip(*map(lambda x:
                                             [x.count(home_office_type[i]) for i in xrange(len(home_office_type))],
                                             zip(*home_office_tmp))))
    home_office = {"category": home_office_type, "xAxis": list(range(24)), "series": series}
    event = {"category": list(zip(*event_tmp)[0]), "series": list(zip(*event_tmp)[1])} \
        if event_tmp else {"category": [], "series": []}
    context = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'home_office': home_office,
            'event': event
        }
    }
    return render_template('dashboard/scene.html',
                           option=json.dumps(context),
                           username=username,
                           app_id=app_id,
                           app_list=app_list)


def get_query_list(app_id='', *field):
    if not app_id:
        app_id = '5621fb0f60b27457e863fabb'
    try:
        query_limit = 100
        query = Query(Object.extend('DashDataSource'))
        query.equal_to('app_id', app_id)
        total_count = query.count()
        query_times = (total_count + query_limit - 1) / query_limit
        result_list = []
        for index in xrange(query_times):
            query.limit(query_limit)
            query.skip(index * query_limit)
            result_list.extend(query.find())
    except LeanCloudError, e:
        print(e)
        return {}
    ret_dict = {}
    for item in field:
        ret_dict[item] = map(lambda result: result.attributes[item], result_list)
    return ret_dict


def translate_motion(s):
    library = {'motionCommuting': '乘车',   'motionWalking': '走路', 'motionSitting': '静坐',
               'motionBiking': '骑车', 'motionRunning': '跑步', '': ''}
    return library[s]


def translate_interest(s):
    library = {"jogging": "慢跑", "fitness": "健身", "basketball": "篮球", "football": "足球",
               "badminton": "羽毛球", "bicycling": " 骑车", "table_tennis": "网球", 'social': "社交",
               'online_shopping': "网络购物", 'offline_shoppng': "线下购物", 'tech_news': "教育新闻",
               'entertainment_news': "娱乐新闻", 'current_news': "时事新闻", 'business_news': "商业新闻",
               'sports_news': "运动新闻",  'game_news': "游戏新闻", 'study': "学霸", 'gamer': "游戏玩家",
               'health': "健康", 'sports_show': "体育节目", 'game_show': "游戏节目", "variety_show": "综艺节目",
               'tvseries_show': "电视剧", 'acg': "动漫", 'indoorsman': "宅男", '': ''}
    return library[s]


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

