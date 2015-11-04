# coding: utf-8

from leancloud import Engine, Query, Object
from server import app
from datetime import datetime
import time

engine = Engine(app)


@engine.after_save('UserInfoLog')
def post_static_info(params):
    parse_dict = parse_static_info(params)
    return updata_backend_info(parse_dict)


@engine.after_save('UserLocation')
def post_location_info(params):
    parse_dict = parse_location_info(params)
    return updata_backend_info(parse_dict)


@engine.after_save('UPoiVisitLog')
def post_homeoffice_info(params):
    parse_dict = parse_home_office_info(params)
    return updata_backend_info(parse_dict)


@engine.after_save('UserEvent')
def post_event_info(params):
    parse_dict = parse_event_info(params)
    return updata_backend_info(parse_dict)


@engine.after_save('UserActivity')
def post_activity_info(params):
    parse_dict = parse_avtivity_info(params)
    return updata_backend_info(parse_dict)


# @engine.define
def post_context_info(params):
    parse_dict = parse_context_info(params)
    return updata_backend_info(parse_dict)


def parse_static_info(info_log):
    ret_dict = {}
    user_id = info_log.get('user').id
    ret_dict['user_id'] = user_id
    static_info = info_log.get('staticInfo') or {}

    for key, value in static_info.items():
        if isinstance(value, dict):
            ret_dict[key] = sorted(value.items(), key=lambda value: -value[1])[0][0]
        elif isinstance(value, float):
            if len(key.split('-')) > 1:
                ret_dict[key.split('-')[0]] = key.split('-')[1]
            elif key == 'gender':
                ret_dict[key] = 'male' if value > 0 else 'female'
            else:
                ret_dict[key] = 'yes' if value > 0 else 'no'
    return ret_dict


def parse_location_info(location_info):
    ret_dict = {}
    user_id = location_info.get('user').id
    location = location_info.get('location')
    province = location_info.get('province')
    city = location_info.get('city')
    street = location_info.get('street')
    poiproblv1 = location_info.get('poiProbLv1') or {}
    poiproblv2 = location_info.get('poiProbLv2') or {}
    timestamp = location_info.get('timestamp') or None

    location_tmp = {
        timestamp: {
            'location': location,
            'province': province,
            'city': city,
            'street': street,
            'poiProbLv1': sorted(poiproblv1.items(), key=lambda value: -value[1])[0][0],
            'poiProbLv2': sorted(poiproblv2.items(), key=lambda value: -value[1])[0][0]
        }
    }
    ret_dict['user_id'] = user_id
    ret_dict['location'] = location_tmp
    return ret_dict


def parse_home_office_info(homeoffice_info):
    ret_dict = {}
    user_id = homeoffice_info.get('user').id
    status = homeoffice_info.get('home_office_label')
    visit_time = homeoffice_info.get('visit_time')
    ret_dict['user_id'] = user_id
    ret_dict['home_office_status'] = {visit_time: status}
    return ret_dict


def parse_event_info(event_info):
    ret_dict = {}
    user_id = event_info.get('user').id if event_info.get('user') else None
    events = event_info.get('event') or {}
    startTime = event_info.get('startTime')
    endTime = event_info.get('endTime')
    ret_dict['user_id'] = user_id
    event_tmp = sorted(events.items(), key=lambda value: -value[1])
    event = event_tmp[0][0] if event_tmp else None
    ret_dict['event'] = {
        startTime: {
            'event': event,
            'endTime': endTime
        }
    }
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
    user_id = context_info.get('user').id
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
        for key, value in parse_dict.items():
            if key is 'user_id':
                dst_table.set('user', user)
            elif key is 'home_office_status':
                home_office_status = dst_table.get('home_office_status') or {}
                for k, v in parse_dict['home_office_status'].items():
                    home_office_status[k] = v
                dst_table.set('home_office_status', home_office_status)
            elif key is 'event':
                event = dst_table.get('event') or {}
                for k, v in parse_dict['event'].items():
                    event[k] = v
                dst_table.set('event', event)
            elif key is 'location':
                location = dst_table.get('location') or {}
                for k, v in parse_dict['location'].items():
                    location[k] = v
                dst_table.set('location', location)
            else:
                dst_table.set(key, value)
        dst_table.save()
        return True
