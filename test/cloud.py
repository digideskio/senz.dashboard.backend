# coding: utf-8

from leancloud import Query, Object, init
from datetime import datetime
import time


query_limit = 100

def get_obj_list(obj_name):
    query = Query(Object.extend(obj_name))
    total_count = query.count()
    query_times = (total_count + query_limit - 1) / query_limit
    ret_list = []
    for index in range(query_times):
        query.limit(query_limit)
        query.skip(index * query_limit)
        ret_list.extend(query.find())
    return ret_list


def post_static_info(params):
    parse_dict = parse_static_info(params)
    return updata_backend_info(parse_dict)


def post_location_info(params):
    parse_dict = parse_location_info(params)
    return updata_backend_info(parse_dict)


def post_homeoffice_info(params):
    parse_dict = parse_home_office_info(params)
    return updata_backend_info(parse_dict)


def post_event_info(params):
    parse_dict = parse_event_info(params)
    return updata_backend_info(parse_dict)


def post_activity_info(params):
    parse_dict = parse_avtivity_info(params)
    return updata_backend_info(parse_dict)


def post_context_info(params):
    parse_dict = parse_context_info(params)
    return updata_backend_info(parse_dict)


def parse_static_info(info_log):
    ret_dict = {}
    user_id = info_log.get('user').id
    ret_dict['user_id'] = user_id
    static_info = info_log.get('staticInfo')

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
    user_id = homeoffice_info.get('user').id
    status = homeoffice_info.get('home_office_label')
    visit_time = homeoffice_info.get('visit_time')
    ret_dict['user_id'] = user_id
    ret_dict['home_office_status'] = {visit_time: status}
    return ret_dict


def parse_event_info(event_info):
    ret_dict = {}
    user_id = event_info.get('user').id if event_info.get('user') else None
    events = event_info.get('event')
    startTime = event_info.get('startTime')
    endTime = event_info.get('endTime')
    ret_dict['user_id'] = user_id
    event = sorted(events.items(), key=lambda value: -value[1])[0][0]
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
    print parse_dict
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

        table_dash = Object.extend('Test')
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



if __name__ == '__main__':
    init('z6fhqxvpal43l238q7xzogfdls74my214o5bapm5vkwfn4xh',
         'rb7jufb22o15nzc9ub5b6b0lx3xt845o2ofz494oc1s9esg8')

    obj_name_list = ['UserEvent', 'UserInfoLog', 'UserLocation', 'UserMotion']

    #obj_list = get_obj_list(obj_name_list[0])
    #for obj in obj_list:
    #    post_event_info(obj)

    obj_list = get_obj_list(obj_name_list[1])
    for obj in obj_list:
        post_static_info(obj)

    obj_list = get_obj_list(obj_name_list[2])
    for obj in obj_list:
        post_location_info(obj)
