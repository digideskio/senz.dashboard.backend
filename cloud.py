# coding: utf-8

from leancloud import Engine, Query, Object
from server import app
from common.timer import CountDownExec
from datetime import datetime
import time

engine = Engine(app)


@engine.define
def post_static_info(**params):
    parse_dict = parse_static_info(params)
    return updata_backend_info(parse_dict)


@engine.define
def post_location_info(**params):
    parse_dict = parse_location_info(params)
    return updata_backend_info(parse_dict)


@engine.define
def post_homeoffice_info(**params):
    parse_dict = parse_home_office_info(params)
    return updata_backend_info(parse_dict)


@engine.define
def post_event_info(**params):
    parse_dict = parse_event_info(params)
    return updata_backend_info(parse_dict)


@engine.define
def post_activity_info(**params):
    parse_dict = parse_avtivity_info(params)
    return updata_backend_info(parse_dict)


@engine.define
def post_context_info(**params):
    parse_dict = parse_context_info(params)
    return updata_backend_info(parse_dict)


# @engine.define
# def timeline_distribute(**params):
#     global uid
#     user_id = params.get('user_id')
#     uid = user_id
#     data = {'data': 'test1'}
#     CountDownExec(1, post_fake_to_wilddog, user_id, data).start()
#     return user_id
#
#
# def post_fake_to_wilddog(*param):
#     print(param)
#     print(uid, param[0][0])
#     if uid == param[0][0]:
#         data = {'data': 'testn'}
#         CountDownExec(1, post_fake_to_wilddog, uid, data).start()
#     return True


def parse_static_info(info_log):
    ret_dict = {}
    user_id = info_log.get('user').get('objectId')
    ret_dict['user_id'] = user_id
    static_info = info_log.get('staticInfo')

    for key, value in static_info.items():
        if isinstance(value, dict):
            ret_dict[key] = sorted(value.items(), key=lambda value: -value[1])[0][0]
        elif isinstance(value, float):
            if key == 'gender':
                ret_dict[key] = 'male' if value > 0 else 'female'
            else:
                ret_dict[key] = 'yes' if value > 0 else 'no'
    return ret_dict


def parse_location_info(location_info):
    ret_dict = {}
    user_id = location_info.get('user').get('objectId')
    location = location_info.get('location')
    province = location_info.get('province')
    city = location_info.get('city')
    poiproblv1 = location_info.get('poiProbLv1')
    poiproblv2 = location_info.get('poiProbLv2')

    ret_dict['user_id'] = user_id
    ret_dict['location'] = location
    ret_dict['province'] = province
    ret_dict['city'] = city
    ret_dict['poiProbLv1'] = sorted(poiproblv1.items(), key=lambda value: -value[1])[0][0]
    ret_dict['poiProbLv2'] = sorted(poiproblv2.items(), key=lambda value: -value[1])[0][0]
    return ret_dict


def parse_home_office_info(homeoffice_info):
    ret_dict = {}
    user_id = homeoffice_info.get('user').get('objectId')
    status = homeoffice_info.get('home_office_label')
    visit_time = homeoffice_info.get('visit_time')
    ret_dict['user_id'] = user_id
    ret_dict['home_office_status'] = {visit_time: status}
    return ret_dict


def parse_event_info(event_info):
    ret_dict = {}
    user_id = event_info.get('user').get('objectId')
    events = event_info.get('event')
    ret_dict['user_id'] = user_id
    ret_dict['event'] = sorted(events.items(), key=lambda value: -value[1])[0][0]
    return ret_dict


def parse_avtivity_info(activity_info):
    ret_dict = {}
    user_id = activity_info.get('user_id')
    time_range_start = activity_info.get('time_range_start') or None
    time_range_end = activity_info.get('time_range_end') or None
    time_range_start = time.mktime(datetime.strptime(time_range_start['iso'], '%Y-%m-%dT%H:%M:%S.000Z').timetuple())
    time_range_end = time.mktime(datetime.strptime(time_range_end['iso'], '%Y-%m-%dT%H:%M:%S.000Z').timetuple())
    activities = activity_info.get('matched_activities')
    activities = activities[0] if activities else {}
    activity = activities.get('category')
    ret_dict['activity'] = {'category': activity,
                            'time_range_start': int(time_range_start*1000),
                            'time_range_end': int(time_range_end*1000)}
    ret_dict['user_id'] = user_id
    return ret_dict


def parse_context_info(context_info):
    ret_dict = {}
    user_id = context_info.get('user').get('objectId')
    ret_dict['user_id'] = user_id
    return ret_dict


def updata_backend_info(parse_dict):
    user_id = parse_dict['user_id']
    # get user Object
    query = Query(Object.extend('_User'))
    query.equal_to('objectId', user_id)
    user = query.find()[0] if query.count() else None

    # get app Object
    query = Query(Object.extend('BindingInstallation'))
    query.equal_to('user', user)
    result_list = query.find()
    app_set = set()
    for result in result_list:
        app_set.add(result.attributes['application'].id)
    app_id_list = list(app_set)

    for app_id in app_id_list:
        query = Query(Object.extend('Application'))
        query.equal_to('objectId', app_id)
        app = query.find()[0]

        table_dash = Object.extend('DashboardSource')
        query = Query(table_dash)
        query.equal_to('app', app)
        query.equal_to('user', user)
        dst_table = query.find()
        if not dst_table:
            dst_table = table_dash()
        else:
            dst_table = dst_table[0]

        dst_table.set('app', app)
        dst_table.set('user', user)

        for key, value in parse_dict.items():
            if key is not 'home_office_status':
                dst_table.set(key, value)
            else:
                home_office_status = dst_table.get('home_office_status') or {}
                for k, v in parse_dict['home_office_status'].items():
                    home_office_status[k] = v
                dst_table.set('home_office_status', home_office_status)
        dst_table.save()
        return True
