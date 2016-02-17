from flask import render_template, Blueprint
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json

exhibition_marriage = Blueprint('exhibition_marriage', __name__, template_folder='templates')


@exhibition_marriage.route('/dashboard/marriage')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
        static_info = fake_data.get('static_info')
        marriage_obj = static_info.get('marriage')
        pregnant_obj = static_info.get('pregnant')
        marriage = {'category': map(lambda x: translate(x, 'marriage'), marriage_obj.keys()),
                    'series': map(lambda x: marriage_obj.get(x), marriage_obj.keys())}
        pregnant = {'category': map(lambda x: translate(x, 'pregnant'), pregnant_obj.keys()),
                    'series': map(lambda x: pregnant_obj.get(x), pregnant_obj.keys())}
    else:
        result_dict = get_query_list(app_id, 'marriage', 'pregnant')
        marriage_list = filter(lambda x: x is not None, result_dict['marriage'])
        pregnant_list = filter(lambda x: x is not None, result_dict['pregnant'])
        marriage = {'category': map(lambda x: translate(x, 'marriage'), list(set(marriage_list))),
                    'series': map(lambda x: marriage_list.count(x), list(set(marriage_list)))}
        pregnant = {'category': map(lambda x: translate(x, 'pregnant'), list(set(pregnant_list))),
                    'series': map(lambda x: pregnant_list.count(x), list(set(pregnant_list)))}
    ret_json = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'marriage': marriage,
            'pregnant': pregnant
        }
    }
    return render_template('dashboard/user-matrimony.html', option=json.dumps(ret_json),
                           username=username, app_id=app_id, app_list=app_list)

