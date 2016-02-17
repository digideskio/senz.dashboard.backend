from flask import render_template, Blueprint
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json

exhibition_profile = Blueprint('exhibition_profile', __name__, template_folder='templates')


@exhibition_profile.route('/dashboard/profile')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
        static_info = fake_data.get('static_info')
        gender_obj = static_info.get('gender')
        gender = {'category': map(lambda x: translate(x, 'gender'), gender_obj.keys()),
                  'series': map(lambda x: gender_obj.get(x), gender_obj.keys())}

        age_obj = static_info.get('age')
        age = {'category': map(lambda x: translate(x, 'age'), age_obj.keys()),
               'series': map(lambda x: age_obj.get(x), age_obj.keys())}

        occupation_obj = static_info.get('occupation')
        occupation = {"category": map(lambda x: translate(x, 'occupation'), occupation_obj.keys()),
                      "series": map(lambda x: occupation_obj.get(x), occupation_obj.keys())}

        field_obj = static_info.get('field')
        field = {"category": map(lambda x: translate(x, 'field'), field_obj.keys()),
                 "series": map(lambda x: field_obj.get(x), field_obj.keys())}
    else:
        result_dict = get_query_list(app_id, 'gender', 'age', 'occupation', 'field')
        gender_list = filter(lambda x: x, result_dict.get('gender'))
        age_list = filter(lambda x: x, result_dict.get('age'))
        occupation_list = filter(lambda x: x, result_dict.get('occupation'))
        field_list = filter(lambda x: x, result_dict.get('field'))
        gender = {'category': map(lambda x: translate(x, 'gender'), list(set(gender_list))),
                  'series': map(lambda x: gender_list.count(x), list(set(gender_list)))}
        age = {'category': map(lambda x: translate(x, 'age'), list(set(age_list))),
               'series': map(lambda x: age_list.count(x), list(set(age_list)))}

        occupation_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, occupation_list.count(x)],
                                                         filter(lambda x: str(x) != '', set(occupation_list)))))
        occupation = {"category": map(lambda x: translate(x, 'occupation') or '', occupation_tmp[0]),
                      "series": occupation_tmp[1]} if occupation_tmp else {"category": [], "series": []}
        field_tmp = map(lambda x: list(x), zip(*map(lambda x: [x, field_list.count(x)],
                                                    filter(lambda x: str(x) != '', set(field_list)))))
        field = {"category": map(lambda x: translate(x, 'field') or '', field_tmp[0]),
                 "series": field_tmp[1]} if field_tmp else {"category": [], "series": []}

    data = {'gender': gender, 'age': age, 'job': occupation, 'profession': field}
    user_profile = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('dashboard/user-identity.html', option=json.dumps(user_profile),
                           username=username, app_id=app_id, app_list=app_list)