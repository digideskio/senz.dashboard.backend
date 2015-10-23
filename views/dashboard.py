# coding: utf-8
from flask import Blueprint, render_template, json, request, make_response
from leancloud import Object, Query
import time

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def index():
    return render_template('index.html')


@dashboard.route('/dashboard/profile')
def profile():
    app_id = request.args.get('app_id')
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'gender', 'age', 'occupation', 'field')
    gender_list = [] if 'gender' not in result_dict else result_dict['gender']
    age_list = [] if 'age' not in result_dict else result_dict['age']
    occupation_list = [] if 'occupation' not in result_dict else result_dict['occupation']
    field_list = [] if 'field' not in result_dict else result_dict['field']

    gender = {'category': ['male', 'female'], 'series': [gender_list.count('male'), gender_list.count('female')]}
    age = {"category": ["55up", "35to55", "16to35", "16down"],
           "series": [age_list.count('55up'), age_list.count('35to55'),
                      age_list.count('16to35'), age_list.count('16down')]}
    category = []
    series = []
    for item in set(occupation_list):
        category.append(item)
        series.append(occupation_list.count(item))
    job = {"category": category, "series": series}

    category = []
    series = []
    for item in set(field_list):
        category.append(item)
        series.append(field_list.count(item))
    profession = {"category": category,  "series": series}

    data = {'gender': gender, 'age': age, 'job': job, 'profession': profession}
    user_profile = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-identity.html', option=json.dumps(user_profile))


@dashboard.route('/dashboard/interest')
def interest():
    app_id = request.args.get('app_id')
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'interest')
    interest_list = [] if 'interest' not in result_dict else result_dict['interest']

    category = []
    series = []
    for item in set(interest_list):
        category.append(item)
        series.append(interest_list.count(item))
    data = {"category": category,  "series": series}
    interest = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-hobby.html', option=json.dumps(interest))


@dashboard.route('/dashboard/marriage')
def marriage():
    app_id = request.args.get('app_id')
    result_dict = get_query_list(app_id, 'marriage', 'pregnant')
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
    return render_template('dashboard/user-matrimony.html', option=json.dumps(ret_json))


@dashboard.route('/dashboard/consumption')
def consumption():
    s1 = time.clock()
    app_id = request.args.get('app_id')
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'consumption', 'has_car', 'has_pet')
    consumption_list = [] if 'consumption' not in result_dict else result_dict['consumption']
    car_list = [] if 'has_car' not in result_dict else result_dict['has_car']
    pet_list = [] if 'has_pet' not in result_dict else result_dict['has_pet']
    print consumption_list
    print car_list
    print pet_list
    category = []
    series = []
    for item in set(consumption_list):
        category.append(item)
        series.append(consumption_list.count(item))
    consumption = {"category": category,  "series": series}
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
    s2 = time.clock()
    print s2 - s1
    return render_template('dashboard/user-consumption.html', option=json.dumps(ret_json))


@dashboard.route('/dashboard/location')
def location():
    app_id = request.args.get('app_id')
    return render_template('dashboard/user-location.html')


@dashboard.route('/dashboard/motion')
def motion():
    app_id = request.args.get('app_id')

    home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'home_office_status')
    home_office_list = [] if 'home_office_status' not in result_dict else result_dict['home_office_status']

    series = []
    for i in range(4):
        sub_series = []
        for j in range(24):
            sub_series.append(0)
        series.append(sub_series)

    for item in home_office_list:
        for i in range(24):
            for j in range(len(home_office_type)):
                if item['status'+str(i)] == home_office_type[j]:
                    series[j][i] += 1
    data = {"category": home_office_type, "xAxis": list(range(24)), "series": series}
    home_office_status = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/scene.html',  option=json.dumps(home_office_status))


@dashboard.route('/dashboard/event')
def event():
    app_id = request.args.get('app_id')
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'event')
    event_list = [] if 'event' not in result_dict else result_dict['event']

    category = []
    series = []
    for item in set(event_list):
        category.append(item)
        series.append(event_list.count(item))
    data = {"category": category,  "series": series}
    event = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/event.html', option=json.dumps(event))


def get_query_list(app_id='', *field):
    if not app_id:
        return {}

    query_limit = 1000
    query = Query(Object.extend('DashDataSource'))
    query.equal_to('app_id', app_id)
    total_count = query.count()
    query_times = (total_count + query_limit - 1) / query_limit
    result_list = []
    for index in range(query_times):
        query.limit(query_limit)
        query.skip(index * query_limit)
        result_list.extend(query.find())

    ret_dict = {}
    for item in field:
        ret_dict[item] = map(lambda result: result.attributes[item], result_list)
    return ret_dict


