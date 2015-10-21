# coding: utf-8
from flask import Blueprint, render_template, json, request
from leancloud import Object, Query

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show():
    return render_template('index.html')


@dashboard.route('/dashboard/profile')
def profile():
    app_id = request.args.get('app_id')
    gender_list = get_query_list('5621fb0f60b27457e863fabb', 'gender')
    age_list = get_query_list(app_id, 'age')
    occupation_list = get_query_list(app_id, 'occupation')
    field_list = get_query_list(app_id, 'field')

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
    interest_list = get_query_list('5621fb0f60b27457e863fabb', 'interest')
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
    return render_template('dashboard/user-hobby.html', option=interest)


@dashboard.route('/dashboard/marriage')
def marriage():
    app_id = request.args.get('app_id')
    marriage_list = get_query_list(app_id, 'marriage')
    pregnant_list = get_query_list(app_id, 'pregnant')

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
    return render_template('dashboard/user-matrimony.html', option=ret_json)


@dashboard.route('/dashboard/consumption')
def consumption():
    app_id = request.args.get('app_id')
    consumption_list = get_query_list('5621fb0f60b27457e863fabb', 'consumption')
    car_list = get_query_list('5621fb0f60b27457e863fabb', 'has_car')
    pet_list = get_query_list('5621fb0f60b27457e863fabb', 'has_pet')

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
    return render_template('dashboard/user-consumption.html', option=ret_json)


@dashboard.route('/dashboard/location')
def location():
    app_id = request.args.get('app_id')
    return render_template('dashboard/user-location.html')


@dashboard.route('/dashboard/motion')
def motion():
    app_id = request.args.get('app_id')

    home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']
    home_office_list = get_query_list('5621fb0f60b27457e863fabb', 'home_office_status')

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
    return render_template('dashboard/scene.html',  option=home_office_status)


@dashboard.route('/dashboard/event')
def event():
    app_id = request.args.get('app_id')
    event_list = get_query_list('5621fb0f60b27457e863fabb', 'event')
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
    return render_template('dashboard/event.html', option=event)


def get_query_list(app_id='', field=''):
    if not app_id:
        return []

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

    ret_list = []
    for result in result_list:
        ret_list.append(result.attributes[field])
    return ret_list
