from flask import render_template, Blueprint
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json

exhibition_consumption = Blueprint('exhibition_consumption', __name__, template_folder='templates')


@exhibition_consumption.route('/dashboard/consumption')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
        static_info = fake_data.get('static_info')
        consumption_obj = static_info.get('consumption')
        hascar_obj = static_info.get('has_car')
        haspet_obj = static_info.get('has_pet')
        consum = {'category': map(lambda x: translate(x, 'consumption'), consumption_obj.keys()),
                  'series': map(lambda x: consumption_obj.get(x), consumption_obj.keys())}
        car = {'category': map(lambda x: translate(x, 'has_car'), hascar_obj.keys()),
               'series': map(lambda x: hascar_obj.get(x), hascar_obj.keys())}
        pet = {'category': map(lambda x: translate(x, 'has_pet'), haspet_obj.keys()),
               'series': map(lambda x: haspet_obj.get(x), haspet_obj.keys())}
    else:
        result_dict = get_query_list(app_id, 'consumption', 'has_car', 'has_pet')
        consumption_list = filter(lambda x: x is not None, result_dict['consumption'])
        car_list = filter(lambda x: x is not None, result_dict['has_car'])
        pet_list = filter(lambda x: x is not None, result_dict['has_pet'])
        consumption_tmp = map(lambda x: list(x),
                              zip(*map(lambda x: [x, consumption_list.count(x)], set(consumption_list))))
        consum = {"category": map(lambda x: translate(x, 'consumption'), consumption_tmp[0]),
                  "series": consumption_tmp[1]} if consumption_tmp else {}
        car = {'category': map(lambda x: translate(x, 'has_car'), list(set(car_list))),
               'series': map(lambda x: car_list.count(x), list(set(car_list)))}
        pet = {'category': map(lambda x: translate(x, 'has_pet'), list(set(pet_list))),
               'series': map(lambda x: pet_list.count(x), list(set(pet_list)))}

    ret_json = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'consumption': consum,
            'car': car,
            'pet': pet
        }
    }
    return render_template('dashboard/user-consumption.html', option=json.dumps(ret_json),
                           username=username, app_id=app_id, app_list=app_list)

