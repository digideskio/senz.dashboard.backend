# coding: utf-8
from flask import session
from pymongo import MongoClient
from leancloud import Object, Query, LeanCloudError
from application.models import Developer
from application.common.util import translate
from os.path import dirname, join
import requests
import time
import json

DashboardSource = Object.extend('DashboardSource')
DashDataSource = Object.extend('DashDataSource')
DashboardGroup = Object.extend('DashboardGroup')
DashboardStatistics = Object.extend('DashboardStatistics')

client = MongoClient('mongodb://senzhub:Senz2everyone@119.254.111.40/RefinedLog')
CombinedTimelines = client.get_default_database().CombinedTimelines


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


def get_tracker_of_app(app_id=None, group_id=None):
    if not app_id or app_id == u'5621fb0f60b27457e863fabb':
        return [u'user0', u'user1', u'user2', u'user3']
    elif app_id == u'all':
        return [u'5689cf3700b09aa2fdd88d3b', u'5684d18200b068a2a955aefc', u'5689cd6d60b2e57ba2c05e4c',
                u'5684fa9e00b009a31af7efcb', u'5634da2360b22ab52ef82a45', u'56ab329fc4c97100530f5281',
                u'560388c100b09b53b59504d2', u'560d7193ddb2dd00356f4e80', u'560bd9b7ddb2e44a621fc217',
                u'561bdea960b2de2d09810f22', u'5624b97660b296e5979bce05', u'5624ce21ddb24819b84d59d2',
                u'560bdbcb60b267e6db7aa2a9', u'560e7b25ddb2e44a624f4d4e', u'5625af4060b202593e53cda7',
                u'562881ae60b2260e76fc77cb', u'5627226c00b09f851ff4a200', u'564156f160b262671ea7aa65',
                u'564049ae60b262671e9ce28f', u'56404b4200b0ee7f57b44968', u'5624d68460b2b199f7628914',
                u'5604e5ce60b2521fb8eb240a', u'56406b4a00b0ee7f57b5c3a3', u'5624da0960b27457e89bff13',
                u'560d3a9960b2ad8a22f32966', u'564bd84b60b2ed362064985f', u'55d845e100b0d7b2266ac668',
                u'564575ac60b20fc9b99d8d9d', u'56065bba60b2aac0d6f2a38a', u'558a5ee7e4b0acec6b941e96',
                u'55f788f4ddb25bb7713125ef', u'5588d20be4b0dc547bacb2ce', u'5653c88e00b0e772838cd61b',
                u'565d52af60b2824f23970155', u'568a0ca200b01b9f2c08f53d', u'55c1e2d900b0ee7fd66e8ea3',
                u'5682580d00b0f9a1f22748c7', u'5684d3d660b2b60f65d84285', u'569e0eae2e958a0059d8ec1e',
                u'568cd96160b2a09924491657', u'569e0f669123b80055614607', u'559f81fbe4b0ed48f0552737']
    app = {
        "__type": "Pointer",
        "className": "Application",
        "objectId": app_id
    }
    query = Query(DashboardSource)
    query.equal_to('app', app)
    query.select('user')

    label = ['age', 'gender', 'marriage', 'pregnant', 'has_car',
             'has_pet', 'occupation', 'field', 'consumption', 'interest']

    if group_id:
        group_query = Query(DashboardGroup)
        group_query.equal_to("objectId", group_id)
        group = group_query.first() or {}
        for k, v in group.attributes.items():
            if k in label:
                for ele in v:
                    query.equal_to(k, ele)
    installation_list = query.find()
    return sorted(list(set(map(lambda x: x.attributes['user'].id, installation_list))))


def get_fake_data_of_user(uid):
    ret_dict = {}
    u_index = int(uid[-1]) if uid.startswith('user') else 0

    type_list = [u'gender', u'age', u'field', u'occupation', u'interest',
                 u'marriage', u'pregnant', u'consumption', u'has_car', u'has_pet']
    user_labels = [
        [u'男', u'16-35岁', u'IT', u'宅', u'游戏新闻'],
        [u'女', u'16-35岁', u'5000to10000', u'教师', u'已婚', u'线上购物', u'电视剧'],
        [u'男', u'16-35岁', u'5000-10000', u'公务员', u'有车', u'已婚', u'跑步', u'游戏玩家', u'体育新闻'],
        [u'女', u'16-35岁', u'20000以上', u'金融', u'未婚', u'关注健康', u'有车']
    ]
    eventDatas = [
        {
            "category": [u'商圈工作中', u'乘地铁', u'出行', u'在家休息', u'看电影', u'在餐厅吃饭'],
            "data": [25, 25, 30, 23, 3, 2],
            "avg": []
        },
        {
            "category": [u'演唱会', u'逛街', u'出行', u'在家休息', u'看电影', u'在餐厅吃饭'],
            "data": [1, 4, 8, 25, 4, 5],
            "avg": []
        },
        {
            "category": [u'出行', u'乘地铁', u'在家休息', u'户外锻炼', u'看电影'],
            "data": [30, 15, 20, 20, 3],
            "avg": []
        },
        {
            "category": [u'出行', u'乘地铁', u'在家休息', u'户外锻炼', u'室内锻炼'],
            "data": [35, 16, 18, 3, 15],
            "avg": []
        }
    ]
    actionDatas = [
        {
            "category": [u'静坐', u'乘车', u'走路', u'跑步', u'骑车'],
            "data": [200, 70, 20, 5, 2],
            "avg": []
        },
        {
            "category": [u'静坐', u'乘车', u'走路', u'跑步', u'骑车'],
            "data": [180, 15, 30, 15, 8],
            "avg": []
        },
        {
            "category": [u'静坐', u'乘车', u'走路', u'跑步', u'骑车'],
            "data": [180, 42, 25, 30, 15],
            "avg": []
        },
        {
            "category": [u'静坐', u'走路', u'跑步', u'骑车', u'乘车'],
            "data": [280, 8, 30, 10, 30],
            "avg": []
        }
    ]
    homeOfficeDatas = [
        {
            "category": [i for i in xrange(0, 24)],
            "atHomeData": [30,30,30,30,30,30,30,22,0,0,0,0,0,0,0,0,0,0,30,30,30,30,30,30,30],
            "atOfficeData": [0,0,0,0,0,0,0,0,22,22,22,22,22,22,22,22,22,0,0,0,0,0,0,0,0],
            "toHomeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0],
            "toOfficeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0],
            "property": {
                "avg_start": "19:50",
                "avg_end": "7:10",
                "combo_start": "8:40",
                "combo_end": "17:20",
                "duration": "8小时30分钟",
                "home_addr": "南六环",
                "office_addr": "海淀桥北"
            }
        },
        {
            "category": [i for i in xrange(0, 24)],
            "atHomeData": [30,30,30,30,30,22,0,0,0,0,0,0,0,0,0,0,30,30,30,30,30,30,30,30,30],
            "atOfficeData": [0,0,0,0,0,0,22,22,22,22,22,22,22,22,22,22,0,0,0,0,0,0,0,0,0],
            "toHomeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "toOfficeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "property": {
                "avg_start": "16:50",
                "avg_end": "6:30",
                "combo_start": "6:40",
                "combo_end": "16:20",
                "duration": "9小时40分钟",
                "home_addr": "北五环",
                "office_addr": "北五环"
            }
        },
        {
            "category": [i for i in xrange(0, 24)],
            "atHomeData": [30,30,30,30,30,30,30,30,0,0,0,0,0,0,0,0,0,0,30,30,30,30,30,30,30],
            "atOfficeData": [0,0,0,0,0,0,0,0,22,22,22,22,22,22,22,22,22,0,0,0,0,0,0,0,0],
            "toHomeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0],
            "toOfficeData": [0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "property": {
                "avg_start": "19:50",
                "avg_end": "7:10",
                "combo_start": "8:40",
                "combo_end": "17:20",
                "duration": "8小时30分钟",
                "home_addr": "橡树湾",
                "office_addr": "亦庄开发区"
            }
        },
        {
            "category": [i for i in xrange(0, 24)],
            "atHomeData": [30,30,30,30,30,30,30,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30],
            "atOfficeData": [0,0,0,0,0,0,0,0,0,22,22,22,22,22,22,22,22,22,22,22,22,22,22,0,0],
            "toHomeData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0],
            "toOfficeData": [0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "property": {
                "avg_start": "22:30",
                "avg_end": "7:00",
                "combo_start": "8:30",
                "combo_end": "21:00",
                "duration": "12小时30分钟",
                "home_addr": "通州",
                "office_addr": "国贸CBD"
            }
        }
    ]
    locationDatas = [
        {
            "lat": 39.993537,
            "lng": 116.311717,
            "level": 15,
            "heatData": [
                {
                    "lat": 39.720367,
                    "lng": 116.384183,
                    "count": 100
                },
                {
                    "lat": 39.721699,
                    "lng": 116.382135,
                    "count": 100
                },
                {
                    "lat": 39.720922,
                    "lng": 116.387668,
                    "count": 100
                },
                {
                    "lat": 39.721089,
                    "lng": 116.390399,
                    "count": 100
                },
                {
                    "lat": 39.715538,
                    "lng": 116.384219,
                    "count": 100
                },
                {
                    "lat": 39.993537,
                    "lng": 116.311717,
                    "count": 100
                },
                {
                    "lat": 39.993299,
                    "lng": 116.3124,
                    "count": 100
                },
                {
                    "lat": 39.994073,
                    "lng": 116.312211,
                    "count": 100
                },
                {
                    "lat": 39.992936,
                    "lng": 116.313505,
                    "count": 100
                },
                {
                    "lat": 39.993005,
                    "lng": 116.311147,
                    "count": 100
                },
                {
                    "lat": 39.720367,
                    "lng": 116.384183,
                    "count": 100
                },
                {
                    "lat": 39.721699,
                    "lng": 116.382135,
                    "count": 100
                },
                {
                    "lat": 39.720922,
                    "lng": 116.387668,
                    "count": 100
                },
                {
                    "lat": 39.721089,
                    "lng": 116.390399,
                    "count": 100
                },
                {
                    "lat": 39.715538,
                    "lng": 116.384219,
                    "count": 100
                },
                {
                    "lat": 39.993537,
                    "lng": 116.311717,
                    "count": 100
                },
                {
                    "lat": 39.993299,
                    "lng": 116.3124,
                    "count": 100
                },
                {
                    "lat": 39.994073,
                    "lng": 116.312211,
                    "count": 100
                },
                {
                    "lat": 39.992936,
                    "lng": 116.313505,
                    "count": 100
                },
                {
                    "lat": 39.993005,
                    "lng": 116.311147,
                    "count": 100
                }
            ]
        },
        {
            "lat": 40.023846,
            "lng": 116.3229,
            "level": 15,
            "heatData": [{
                "lat": 40.023846,
                "lng": 116.3229,
                "count": 100
            }]
        },
        {
            "lat": 40.037043,
            "lng": 116.338469,
            "level": 15,
            "heatData": [
                {
                    "lat": 40.037043,
                    "lng": 116.338469,
                    "count": 100
                },
                {
                    "lat": 39.801202,
                    "lng": 116.512988,
                    "count": 100
                }
            ]
        },
        {
            "lat": 39.939434,
            "lng": 116.727444,
            "level": 15,
            "heatData": [
                {
                    "lat": 39.914319,
                    "lng": 116.467524,
                    "count": 100
                },
                {
                    "lat": 39.939434,
                    "lng": 116.727444,
                    "count": 100
                }
            ]
        }
    ]
    detailDatas = [
        {
            "data": []
        },
        {
            "data": []
        },
        {
            "data": []
        },
        {
            "data": []
        }
    ]

    for item in type_list:
        user_labels[u_index] = map(lambda x: translate(x, item), user_labels[u_index])

    fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
    detail_data = fake_data.get("detailData")
    for de in detail_data:
        de['start_ts'] = (int(time.mktime((time.localtime()[0], time.localtime()[1], time.localtime()[2],
                                          8, 39, 0, 0, 0, 0))) - int(de.get('start_ts')))*1000
    ret_dict['userLabels'] = user_labels[u_index]
    ret_dict['eventData'] = eventDatas[u_index]
    ret_dict['actionData'] = actionDatas[u_index]
    ret_dict['homeOfficeData'] = homeOfficeDatas[u_index]
    ret_dict['locationData'] = locationDatas[u_index]
    ret_dict['detailData'] = detail_data
    return ret_dict


def get_motion_stastic(motion, motion_counts):
    query = Query(DashboardSource)
    user_count = query.count()

    for i in xrange(1, len(motion_counts)):
        for k in motion_counts[i].keys():
            if k in motion_counts[0]:
                motion_counts[0][k] += motion_counts[i].get(k)
            else:
                motion_counts[0][k] = motion_counts[i].get(k)
    motion_count = motion_counts[0] if motion_counts else {}

    motion_np = list(set(motion.values()))


    action_data = {
        "category": map(lambda x: translate(x, "motion"), list(set(motion.values()))),
        "data": map(lambda x: motion.values().count(x), motion_np),
        "avg": map(lambda x: (motion_count.get(x) or 0)/user_count, motion_np)
    }
    return action_data


def get_attr_of_user(uid, h_start=None, h_end=None, e_start=None, e_end=None, workday=True):
    ret_dict = {}
    if uid.startswith("user"):
        return get_fake_data_of_user(uid)

    user = {
        "__type": "Pointer",
        "className": "_User",
        "objectId": uid
    }
    type_list = [u'gender', u'age', u'field', u'occupation', u'interest',
                 u'marriage', u'pregnant', u'consumption', u'has_car', u'has_pet']
    query = Query(DashboardSource)
    user_count = query.count()
    query.equal_to('user', user)
    attrs = query.first()

    avg_query = Query(DashboardStatistics)
    counts = avg_query.find()

    timeline = CombinedTimelines.find({"user_id": uid}).sort("start_datetime", -1) or []

    labels = map(lambda x: attrs.attributes.get(x), type_list)
    user_labels = [y for x in filter(lambda y: y, labels) for y in x if isinstance(x, list)]
    user_labels += [type_list[labels.index(x)] for x in labels if isinstance(x, unicode) and x in [u'yes', u'no']]
    user_labels += [x for x in labels if isinstance(x, unicode) and x not in [u'yes', u'no']]
    user_labels = filter(lambda x: x, user_labels)
    for item in type_list:
        user_labels = map(lambda x: translate(x, item), user_labels)
    ret_dict['userLabels'] = user_labels

    event = attrs.attributes.get('event') or {}
    event_counts = map(lambda x: x.attributes.get('event') or {},
                       filter(lambda y: str(e_start) < str(y.attributes.get('timestamp'))[:10] < str(e_end), counts))
    for i in xrange(1, len(event_counts)):
        for k in event_counts[i].keys():
            if k in event_counts[0]:
                event_counts[0][k] += event_counts[i].get(k)
            else:
                event_counts[0][k] = event_counts[i].get(k)
    event_count = event_counts[0] if event_counts else {}

    event = dict(filter(lambda x: str(e_start) < str(x[0]) < str(e_end), event.items()))
    event_np = list(set(event.values()))
    event_data = {
        "category": map(lambda x: translate(translate(x, "event_old"), "context"), event_np),
        "data": map(lambda x: event.values().count(x), event_np),
        "avg": map(lambda x: (event_count.get(x) or 0)/user_count, event_np)
    }
    ret_dict['eventData'] = event_data

    motion_counts = map(lambda x: x.attributes.get('motion') or {},
                        filter(lambda y: str(e_start) < str(y.attributes.get('timestamp'))[:10] < str(e_end), counts))
    motion = attrs.attributes.get('motion') or {}
    motion = dict(filter(lambda x: str(h_start) < str(x[0]) < str(h_end), motion.items()))
    ret_dict['actionData'] = get_motion_stastic(motion, motion_counts)

    home_office = attrs.attributes.get('home_office_status') or {}
    workday_limit = 5 if workday else 7
    home_office = dict(filter(lambda x: str(h_start) < str(x[0]) < str(h_end) and
                                        time.localtime(int(x[0]))[6] < workday_limit, home_office.items()))
    try:
        home_office_property = requests.get("http://api.trysenz.com/stalker/get_home_office/user_id/" + uid)
        home_office_property = json.loads(home_office_property.content) if home_office_property.status_code == 200 else {}
    except Exception, e:
        print e
        home_office_property = {}
    home = home_office_property.get("home") or {}
    office = home_office_property.get("offices") or {}

    avg_start = str(int(home.get("combo_start") or 0)/3600) + ":" + str((int(home.get("combo_start") or 0) % 3600)/60)
    avg_end = str(int(home.get("combo_end") or 0)/3600) + ":" + str((int(home.get("combo_end") or 0) % 3600)/60)
    combo_start = str(int(office.get("combo_start") or 0)/3600) + ":" + str((int(office.get("combo_start") or 0) % 3600)/60)
    combo_end = str(int(office.get("combo_end") or 0)/3600) + ":" + str((int(office.get("combo_end") or 0) % 3600)/60)
    duration = office.get("combo_duration") or 0
    duration = str(int(duration/3600)) + u'小时' + str(int((duration % 3600)/60)) + u'分钟'

    home_upoi = home.get("u_poi_visit_logs")[-1].get("u_poi") if home.get("u_poi_visit_logs") else {}
    office_upoi = office.get("u_poi_visit_logs")[-1].get("u_poi") if office.get("u_poi_visit_logs") else {}

    home_addr = home_upoi.get('poi_address') or ""
    office_addr = office_upoi.get('poi_address') or ""

    home_office_data = {
        "category": [i for i in xrange(0, 24)],
        "atHomeData": map(lambda x: len(filter(lambda z: z[1] == u"at_home" or z[1] == u"contextAtHome" and time.localtime(int(z[0][:10]))[3] == x,
                                               home_office.items())), xrange(0, 24)),
        "atOfficeData": map(lambda x: len(filter(lambda z: z[1] == u"at_office" or z[1] == u"contextAtWork" and time.localtime(int(z[0][:10]))[3] == x,
                                                 home_office.items())), xrange(0, 24)),
        "toHomeData": map(lambda x: len(filter(lambda z: z[1] == u"going_home" or z[1] == u"contextCommutingHome" and time.localtime(int(z[0][:10]))[3] == x,
                                               home_office.items())), xrange(0, 24)),
        "toOfficeData": map(lambda x: len(filter(lambda z: z[1] == u"going_office" or z[1] == u"contextCommutingWork" and time.localtime(int(z[0][:10]))[3] == x,
                                                 home_office.items())), xrange(0, 24)),
        "property": {
            "avg_start": avg_start,
            "avg_end": avg_end,
            "combo_start": combo_start,
            "combo_end": combo_end,
            "duration": duration,
            "home_addr": home_addr,
            "office_addr": office_addr
        }
    }
    ret_dict['homeOfficeData'] = home_office_data

    coordinate = map(lambda x: {"lat": x.get('lat') if isinstance(x, dict) else x.dump().get('latitude'),
                                "lng": x.get('lng') if isinstance(x, dict) else x.dump().get('longitude'),
                                "count": 1}, attrs.attributes.get('coordinate') or [])
    ret_dict['locationData'] = {
        "lng": coordinate[len(coordinate)/2]["lng"] if coordinate else None,
        "lat": coordinate[len(coordinate)/2]["lat"] if coordinate else None,
        "level": 15,
        "heatData": coordinate
    }
    detail_data = []
    for x in timeline:
        motion_count = x.get('motion_count') or {}
        x['motion_count'] = dict(map(lambda y: (translate(translate(y, "motion_old"), "motion"),
                                                motion_count.get(y)), motion_count.keys()))
        x['label'] = translate(translate(x.get('label') or "", "event_old"), "home_office_status_old")
        x['level2_event'] = translate(x.get('level2_event') or "", "level2_event")
        # print x['level2_event']
        detail_data.append(x)
    ret_dict['detailData'] = detail_data
    return ret_dict




