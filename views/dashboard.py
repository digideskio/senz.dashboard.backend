# coding: utf-8
from flask import Blueprint, render_template, jsonify, request
from leancloud import Object, Query

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show():
    return render_template('dashboard/index.html')


@dashboard.route('/dashboard/profile')
def profile():
    app_id = request.args.get('app_id')
    gender_list = get_query_list(app_id, 'gender')
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
    return render_template('dashboard/user-identity.html')


@dashboard.route('/dashboard/interest')
def interest():
    app_id = request.args.get('app_id')
    data = {}
    interest = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-hobby.html')


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
    return render_template('dashboard/user-matrimony.html')


@dashboard.route('/dashboard/consumption')
def consumption():
    app_id = request.args.get('app_id')
    consumption_list = get_query_list(app_id, 'consumption')
    car_list = get_query_list(app_id, 'has_car')
    pet_list = get_query_list(app_id, 'has_pet')

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
    return render_template('dashboard/user-consumption.html')


@dashboard.route('/dashboard/location')
def location():
    app_id = request.args.get('app_id')
    return render_template('dashboard/user-location.html')


@dashboard.route('/dashboard/motion')
def motion():
    return render_template('dashboard/scene.html')


@dashboard.route('/dashboard/event')
def event():
    return render_template('dashboard/event.html')


def get_query_list(app_id='', field=''):
    if not app_id:
        return []
    query = Query(Object.extend('DashboardSource'))
    query.equal_to('app_id', app_id)
    result_list = query.find()

    ret_list = []
    for result in result_list:
        ret_list.append(result.attributes[field])
    return ret_list
