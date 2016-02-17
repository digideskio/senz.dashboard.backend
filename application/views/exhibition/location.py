# coding: utf-8
from flask import render_template, Blueprint
from common import get_app_list, get_query_list
import json

exhibition_location = Blueprint('exhibition_location', __name__, template_folder='templates')


@exhibition_location.route('/dashboard/location')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    result_dict = get_query_list(app_id, 'province', 'city')
    provice_list = map(lambda y: y if y[-1] not in ["省", "市"] else y[0:-1],
                       filter(lambda x: x is not None, result_dict['province']))
    city_list = filter(lambda x: x is not None, result_dict['city'])

    province = map(lambda x: {'name': x[0], 'value': x[1]},
                   sorted(map(lambda x: (x, provice_list.count(x)), set(provice_list)), key=lambda x: -x[1]))
    city = map(lambda x: {'name': x[0], 'value': x[1]},
               sorted(map(lambda x: (x, city_list.count(x)), set(city_list)), key=lambda x: -x[1]))
    location = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'province': province[:6],
            'city': city[:6]
        }
    }
    return render_template('dashboard/user-location.html', option=json.dumps(location),
                           app_id=app_id, app_list=app_list, username=username)