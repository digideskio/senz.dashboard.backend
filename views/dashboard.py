# coding: utf-8
from flask import Blueprint, render_template, json, request, session
from leancloud import Object, Query
from models import Developer

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    return render_template('index.html',
                           username=session.get('username'),
                           app_dict=app_dict)


@dashboard.route('/dashboard/profile')
def profile():
    # app_id = request.args.get('app_id')
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)

    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'gender', 'age', 'occupation', 'field')
    gender_list = [] if 'gender' not in result_dict else result_dict['gender']
    age_list = [] if 'age' not in result_dict else result_dict['age']
    occupation_list = [] if 'occupation' not in result_dict else result_dict['occupation']
    field_list = [] if 'field' not in result_dict else result_dict['field']

    gender = {'category': ['male', 'female'], 'series': [gender_list.count('male'), gender_list.count('female')]}
    age = {"category": ["55up", "35to55", "16to35", "16down"],
           "series": [age_list.count('55up'), age_list.count('35to55'),
                      age_list.count('16to35'), age_list.count('16down')]}
    occupation_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, occupation_list.count(x)], set(occupation_list))))
    occupation = {"category": occupation_tmp[0], "series": occupation_tmp[1]}
    field_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, field_list.count(x)], set(field_list))))
    field = {"category": field_tmp[0], "series": field_tmp[1]}

    data = {'gender': gender, 'age': age, 'job': occupation, 'profession': field}
    user_profile = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-identity.html',
                           option=json.dumps(user_profile),
                           username=session.get('username'),
                           app_dict=app_dict)


@dashboard.route('/dashboard/interest')
def interest():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'interest')
    interest_list = [] if 'interest' not in result_dict else result_dict['interest']
    interest_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, interest_list.count(x)], set(interest_list))))

    data = {"category": interest_tmp[0],  "series": interest_tmp[1]}
    interest = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-hobby.html',
                           option=json.dumps(interest),
                           username=session.get('username'),
                           app_dict=app_dict)


@dashboard.route('/dashboard/marriage')
def marriage():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'marriage', 'pregnant')
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
                           app_dict=app_dict)


@dashboard.route('/dashboard/consumption')
def consumption():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'consumption', 'has_car', 'has_pet')
    consumption_list = [] if 'consumption' not in result_dict else result_dict['consumption']
    car_list = [] if 'has_car' not in result_dict else result_dict['has_car']
    pet_list = [] if 'has_pet' not in result_dict else result_dict['has_pet']

    consumption_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, consumption_list.count(x)], set(consumption_list))))
    consumption = {"category": consumption_tmp[0],  "series": consumption_tmp[1]}
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
                           app_dict=app_dict)


@dashboard.route('/dashboard/location')
def location():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    return render_template('dashboard/user-location.html', username=session.get('username'))


@dashboard.route('/dashboard/motion')
def motion():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    home_office_type = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome']
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'home_office_status')
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
                           app_dict=app_dict)


@dashboard.route('/dashboard/event')
def event():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    result_dict = get_query_list('5621fb0f60b27457e863fabb', 'event')
    event_list = [] if 'event' not in result_dict else result_dict['event']

    list_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, event_list.count(x)], set(event_list))))
    data = {"category": list_tmp[0],  "series": list_tmp[1]}
    event = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    print event
    return render_template('dashboard/event.html',
                           option=json.dumps(event),
                           username=session.get('username'),
                           app_dict=app_dict)


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


