from flask import session
from leancloud import Object, Query, LeanCloudError
from application.models import Developer

DashboardSource = Object.extend('DashboardSource')
DashDataSource = Object.extend('DashDataSource')
DashboardGroup = Object.extend('DashboardGroup')
DashboardStatistics = Object.extend('DashboardStatistics')


def get_app_list():
    ret_dict = {}
    app_id = session.get('app_id')
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()
    ret_dict['app_id'] = app_id
    ret_dict['username'] = username
    ret_dict['app_list'] = app_list
    return ret_dict


def get_query_list(app_id='', *field):
    app_id = app_id or '5621fb0f60b27457e863fabb'
    app = {
        "__type": "Pointer",
        "className": "Application",
        "objectId": app_id
    }
    try:
        query_limit = 100
        if app_id == u'5621fb0f60b27457e863fabb':
            query = Query(DashDataSource)
            query.equal_to('app_id', app_id)
        elif app_id == u'all':
            query = Query(DashboardSource)
        else:
            query = Query(DashboardSource)
            query.equal_to('app', app)
        for item in field:
            query.select(item)
        total_count = query.count()
        query_times = (total_count + query_limit - 1) / query_limit
        result_list = []
        for index in xrange(query_times):
            query.limit(query_limit)
            query.skip(index * query_limit)
            result_list.extend(query.find())
    except LeanCloudError:
        return {}

    ret_dict = {}
    for item in field:
        if app_id == '5621fb0f60b27457e863fabb':
            ret_dict[item] = map(lambda result: result.attributes.get(item), result_list)
        else:
            if item == 'event':
                events_list = filter(lambda x: x,
                                     map(lambda result: result.attributes.get(item), result_list))
                ret_dict[item] = events_list
            elif item == 'home_office_status':
                status = filter(lambda x: x is not None,
                                map(lambda result: result.attributes.get(item), result_list))
                ret_dict[item] = status
            elif item == 'province':
                locations = filter(lambda x: x is not None,
                                   map(lambda result: result.attributes.get('location'), result_list))
                ret_dict[item] = map(lambda x: x.get(item), locations)
            elif item == 'city':
                locations = filter(lambda x: x is not None,
                                   map(lambda result: result.attributes.get('location'), result_list))
                ret_dict[item] = map(lambda x: x.get(item), locations)
            else:
                ret_dict[item] = map(lambda result: result.attributes.get(item), result_list)
    return ret_dict


