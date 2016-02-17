# coding: utf-8
from flask import render_template, Blueprint, request
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json
import time

exhibition_context = Blueprint('exhibition_context', __name__, template_folder='templates')


@exhibition_context.route('/dashboard/context')
def show():
    # filter by timestamp
    h_start = request.form.get('h_start') or request.args.get('h_start') or (int(time.time()) - 30*24*60*60)*1000
    h_end = request.form.get('h_end') or request.args.get('h_end') or int(time.time())*1000
    e_start = request.form.get('e_start') or request.args.get('e_start') or (int(time.time()) - 30*24*60*60)*1000
    e_end = request.form.get('e_end') or request.args.get('e_end') or int(time.time())*1000
    workday = request.form.get('workday') or request.args.get('workday') or "workday"

    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    s = json.load(file(join(dirname(dirname(dirname(__file__))), 'translate.json')))
    home_office_type = s.get('home_office_status').keys()

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
        home_office_status = fake_data.get('home_office_status')
        home_office = {'category': map(lambda x: translate(x, 'home_office_status'), home_office_status.keys()),
                       'series': map(lambda x: home_office_status[x], home_office_status.keys()),
                       "xAxis": list(range(24))}

        context_fake = fake_data.get('context')
        event = {'category': map(lambda x: translate(translate(x, 'event_old'), 'context'), context_fake.keys()),
                 'series': map(lambda x: context_fake[x], context_fake.keys())}
    else:
        # get data from leancloud#DashboardSource
        result_dict = get_query_list(app_id, 'home_office_status', 'event')
        home_office_list = filter(lambda x: x, result_dict['home_office_status'])
        event_list = filter(lambda x: x, result_dict['event'])

        # filter by timestamp
        # if app_id and app_id != '5621fb0f60b27457e863fabb':  # 非DemoFake 假数据
        home_office_list_tmp = map(lambda item:
                                   dict(map(lambda x: (x, item[x]),
                                            filter(lambda y: str(h_start) <= str(y) <= str(h_end)
                                                             and time.localtime(int(str(y)[:10]))[6] < 5
                                            if workday == 'workday' else time.localtime(int(str(y)[:10]))[6] > 4,
                                                   item.keys()))), home_office_list)
        home_office_list = map(lambda x:
                               dict(map(lambda y: ('status' + str(time.localtime(int(y[0])/1000)[3]), y[1]),
                                        x.items())), home_office_list_tmp)

        event_list_tmp = map(lambda item: map(lambda x: item[x],
                                              filter(lambda y: str(e_start) <= str(y) <= str(e_end)
                                                               and time.localtime(int(str(y)[:10]))[6] < 5
                                              if workday == 'workday' else time.localtime(int(str(y)[:10]))[6] > 4,
                                                     item.keys())), event_list)
        event_list = [i for row in event_list_tmp for i in row]

        # filled all the status* field
        for home_office in home_office_list:
            for k in range(0, 24):
                if 'status' + str(k) not in home_office.keys():
                    home_office['status' + str(k)] = None

        home_office_tmp = map(lambda x: map(lambda y: y[1],
                                            sorted(x.items(), key=lambda key: int(key[0][6:]))), home_office_list)
        home_office_series = map(lambda x: list(x),
                                 zip(*map(lambda x: [x.count(home_office_type[y])
                                                     for y in xrange(len(home_office_type))], zip(*home_office_tmp))))
        home_office = {"category": map(lambda x: translate(x, 'home_office_status'), home_office_type),
                       "xAxis": list(range(24)), "series": home_office_series}

        event_list = map(lambda x: translate(translate(x, 'event_old'), 'context'),
                         filter(lambda x: x not in home_office_type, event_list))
        event_tmp = sorted(map(lambda x: (x, event_list.count(x)), set(event_list)), key=lambda item: -item[1])
        event = {"category": list(zip(*event_tmp)[0]), "series": list(zip(*event_tmp)[1])} \
            if event_tmp else {"category": [], "series": []}

    context = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'home_office': home_office,
            'event': event
        }
    }
    if request.method == 'POST':
        return json.dumps(context)
    print "@@@@@@@@@@@@@@@@@@@@@@"
    return render_template('dashboard/context.html', option=json.dumps(context),
                           username=username, app_id=app_id, app_list=app_list)
