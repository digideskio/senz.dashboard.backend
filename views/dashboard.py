# coding: utf-8
from flask import Blueprint, render_template, json, session
from leancloud import Object, Query, LeanCloudError
from models import Developer
import server

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('event')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'event')
        server.cache.set('event', result_dict, timeout=10*60)
    event_list = [] if 'event' not in result_dict else result_dict['event']
    event_list = map(lambda x: server.translate_context(x), event_list)
    event_tmp = sorted(map(lambda x: (x, event_list.count(x)), set(event_list)), key=lambda item: -item[1])
    data = map(lambda x: {'rank': x, 'name': event_tmp[x-1][0]}, xrange(1, 9))
    data.append({'rank': 9, 'name': '...'})
    event = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }

    return render_template('index.html',
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list,
                           option=json.dumps(event))


@dashboard.route('/dashboard/profile')
def profile():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('profile')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'gender', 'age', 'occupation', 'field')
        server.cache.set('profile', result_dict, timeout=10*60)
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
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


@dashboard.route('/dashboard/interest')
def interest():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('interest')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'interest')
        server.cache.set('interest', result_dict, timeout=10*60)
    interest_list = [] if 'interest' not in result_dict else result_dict['interest']
    interest_tmp = sorted(map(lambda x: (x, interest_list.count(x)), set(interest_list)), key=lambda item: -item[1])
    data = map(lambda x: {'rank': x, 'name': interest_tmp[x-1][0]}, xrange(1, 9))
    data.append({'rank': 9, 'name': '...'})
    interest = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-hobby.html',
                           option=json.dumps(interest),
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


@dashboard.route('/dashboard/marriage')
def marriage():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('marriage')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'marriage', 'pregnant')
        server.cache.set('marriage', result_dict, timeout=10*60)
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
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


@dashboard.route('/dashboard/consumption')
def consumption():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('consumption')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'consumption', 'has_car', 'has_pet')
        server.cache.set('consumption', result_dict, timeout=10*60)
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
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


@dashboard.route('/dashboard/location')
def location():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    result_dict = server.cache.get('location')
    if not result_dict:
        result_dict = get_query_list('5621fb0f60b27457e863fabb', 'province', 'city')
        server.cache.set('location', result_dict, timeout=10*60)
    provice_list = [] if 'province' not in result_dict else result_dict['province']
    city_list = [] if 'city' not in result_dict else result_dict['city']
    provice_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, provice_list.count(x)], set(provice_list))))
    city_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, city_list.count(x)], set(city_list))))
    return render_template('dashboard/user-location.html',
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list,
                           provice_tmp=provice_tmp[0][1],
                           city_tmp=city_tmp[0][1])


@dashboard.route('/dashboard/motion')
def motion():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'home_office_status', 'event')
    home_office_list = [] if 'home_office_status' not in result_dict else result_dict['home_office_status']
    list_tmp = map(lambda x: map(lambda y: y[1], sorted(x.items(), key=lambda key: int(key[0][6:]))), home_office_list)
    series = map(lambda x: list(x), zip(*map(lambda x:
                                             [x.count(home_office_type[i]) for i in xrange(len(home_office_type))],
                                             zip(*list_tmp))))
    data = {"category": home_office_type, "xAxis": list(range(24)), "series": series}
    home_office_status = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/scene.html',
                           option=json.dumps(home_office_status),
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)


def get_query_list(app_id='', *field):
    if not app_id:
        return {}
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


