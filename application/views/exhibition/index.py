from exhibition import exhibition_bp
from flask import render_template
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json


@exhibition_bp.route('/dashboard1')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
        context_fake = fake_data.get('context')
        event_tmp = sorted(map(lambda x: (translate(translate(x, 'event_old'), 'context'), context_fake[x]),
                               context_fake.keys()), key=lambda item: -item[1])
    else:
        result_dict = get_query_list(app_id, 'event')
        event_list = filter(lambda x: x is not None, result_dict['event'])
        event_list_tmp = map(lambda item: map(lambda x: item[x],  item.keys()), event_list)
        event_list = [i for row in event_list_tmp for i in row]
        event_list = filter(lambda y: y is not None,
                            map(lambda x: translate(translate(x, 'event_old'), 'context'), event_list))
        event_tmp = sorted(map(lambda x: (x, event_list.count(x)), set(event_list)), key=lambda item: -item[1])
    data = map(lambda x: {'rank': x/3+1, 'name': event_tmp[x-1][0],
                          'count': event_tmp[x-1][1]}, xrange(1, len(set(event_tmp))+1))
    event = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return render_template('index.html', username=username, app_id=app_id,
                           app_list=app_list, option=json.dumps(event))