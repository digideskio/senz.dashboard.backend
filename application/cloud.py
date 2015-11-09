# coding: utf-8

from leancloud import Engine, Query, Object
from datetime import datetime
from application.views.panel import post_panel_data
from application.views.dashboard import translate
from server import app
import time

engine = Engine(app)


@engine.define
def post_obj_from_timeline(name, obj):
    if name == 'UserLocation':
        parse_dict = parse_location_info(obj)
    elif name == 'UPoiVisitLog':
        parse_dict = parse_home_office_info(obj)
    elif name == 'UserInfoLog':
        parse_dict = parse_static_info(obj)
    elif name == 'UserMotion':
        parse_dict = parse_motion_info(obj)
    elif name == 'UserEvent':
        parse_dict = parse_event_info(obj)
    elif name == 'UserActivity':
        parse_dict = parse_avtivity_info(obj)
    else:
        parse_dict = {}
    return updata_backend_info(parse_dict)


def parse_motion_info(motion_obj):
    ret_dict = {}
    user_id = motion_obj.get('user').get('objectId')
    ret_dict['user_id'] = user_id
    timestamp = motion_obj.get('timestamp') or None
    motion_prob = motion_obj.get('motionProb') or {}
    motion = translate(sorted(filter(lambda x: x is not None, motion_prob.items()),
                              key=lambda v: -v[1])[0][0], 'motion_old')
    ret_dict['motion'] = {
        timestamp: {
            'motion': motion
        }
    }
    post_panel_data(tracker=user_id, motion_type='motion', motion_val=motion)
    return ret_dict


def parse_static_info(info_log):
    ret_dict = {}
    user_id = info_log.get('user').get('objectId')
    ret_dict['user_id'] = user_id
    static_info = info_log.get('staticInfo') or {}

    for key, value in static_info.items():
        if isinstance(value, dict):
            ret_dict[key] = sorted(value.items(), key=lambda v: -v[1])[0][0]
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
    user_id = location_info.get('user').get('objectId')
    location = location_info.get('location')
    province = location_info.get('province')
    city = location_info.get('city')
    street = location_info.get('street')
    poiproblv1 = location_info.get('poiProbLv1') or {}
    poiproblv2 = location_info.get('poiProbLv2') or {}
    timestamp = location_info.get('timestamp') or None

    location_tmp = {
        'timestamp': timestamp,
        'location': location,
        'province': province,
        'city': city,
        'street': street,
        'poiProbLv1': sorted(poiproblv1.items(), key=lambda value: -value[1])[0][0],
        'poiProbLv2': sorted(poiproblv2.items(), key=lambda value: -value[1])[0][0]
    }
    ret_dict['user_id'] = user_id
    ret_dict['location'] = location_tmp
    return ret_dict


def parse_home_office_info(homeoffice_info):
    ret_dict = {}
    user_id = homeoffice_info.get('user').get('objectId')
    status = translate(homeoffice_info.get('home_office_label'), 'home_office_status_old')
    visit_time = homeoffice_info.get('visit_time')
    ret_dict['user_id'] = user_id
    ret_dict['home_office_status'] = {visit_time: status}
    post_panel_data(tracker=user_id, context_type='context', context_val=status)
    return ret_dict


def parse_event_info(event_info):
    ret_dict = {}
    user_id = event_info.get('user').get('objectId') if event_info.get('user') else None
    events = event_info.get('event') or {}
    start_time = event_info.get('startTime')
    end_time = event_info.get('endTime')
    ret_dict['user_id'] = user_id
    event_tmp = sorted(events.items(), key=lambda value: -value[1])
    event = translate(event_tmp[0][0], 'event_old') if event_tmp else None
    ret_dict['event'] = {
        start_time: {
            'event': event,
            'endTime': end_time
        }
    }
    post_panel_data(tracker=user_id, context_type='context', context_val=event)
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
    post_panel_data(tracker=user_id, context_type='context', context_val=activity)
    return ret_dict


def updata_backend_info(parse_dict):
    print(parse_dict)
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
            else:
                dst_table.set(key, value)
        dst_table.save()
        return True
