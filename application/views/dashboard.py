# coding: utf-8
from flask import Blueprint, render_template, json, session, request, make_response, redirect, url_for, flash
from leancloud import Object, Query, LeanCloudError
from application.common.util import translate, post_data
from application.models import Developer
from os.path import dirname, join
from bson.json_util import dumps
from pymongo import *
import requests
import time

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates')

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
    # if username == "yzg963@163.com":
    #     app_list.append("564573f660b25b79f067aeef")
    ret_dict['app_list'] = app_list
    return ret_dict


@dashboard_bp.route('/dashboard')
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


@dashboard_bp.route('/dashboard/profile')
def profile():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
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


@dashboard_bp.route('/dashboard/interest', methods=['GET', 'POST'])
def interest():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']
    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
        interest_obj = fake_data.get('interest')
        interest_tmp = interest_obj.items()
    else:
        result_dict = get_query_list(app_id, 'interest')
        interest_list = filter(lambda x: x is not None, result_dict['interest'])
        interest_tmp = [x for y in interest_list for x in y]
        interest_tmp = map(lambda x: (x, interest_tmp.count(x)), list(set(interest_tmp)))
    # map(lambda x: x, interest_tmp)
    sport_type = ["jogging", "fitness", "basketball", "football",
                  "badminton", "bicycling", "table_tennis"]
    shopping_type = ['online_shopping', 'offline_shopping']
    news_type = ["tech_news", "entertainment_news", "current_news",
                 "business_news", "sports_news", "game_news"]
    show_type = ["sports_show", "game_show", "variety_show", "tvseries_show"]
    interest_dict = {}
    for interest in interest_tmp:
        if interest[0] in sport_type:
            if not interest_dict.get('sport'):
                interest_dict['sport'] = {}
            interest_dict['sport'][interest[0]] = interest[1]
        elif interest[0] in shopping_type:
            if not interest_dict.get('shopping'):
                interest_dict['shopping'] = {}
            interest_dict['shopping'][interest[0]] = interest[1]
        elif interest[0] in news_type:
            if not interest_dict.get('news'):
                interest_dict['news'] = {}
            interest_dict['news'][interest[0]] = interest[1]
        elif interest[0] in show_type:
            if not interest_dict.get('show'):
                interest_dict['show'] = {}
            interest_dict['show'][interest[0]] = interest[1]
        else:
            interest_dict[interest[0]] = interest[1]

    color_dict = {'sport': "#7fd6e0", 'shopping': "#c9c5ea", "health": "#97f3da",
                  "social": "#f7cdcf", "news": "#7fbfff", "show": "#7fe7e0",
                  "gamer": "#aef3ee", "indoorsman": "#fbda95", "study": "#84d4ed", "acg": "#a1c4e4"}

    data = map(lambda x: {'color': color_dict.get(x[0]), 'name': translate(x[0], 'interest'),
                          'value': x[1], 'node': []},
               filter(lambda y: not isinstance(y[1], dict), interest_dict.items()))
    data += map(lambda x: {'color': color_dict.get(x[0]), 'name': translate(x[0], 'interest'),
                           'value': sum(x[1].values()),
                           'node': map(lambda z: {'name': translate(z[0], 'interest'),
                                                  "value": z[1]}, x[1].items())},
                filter(lambda y: isinstance(y[1], dict), interest_dict.items()))

    interest_data = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    if request.method == 'POST':
        return json.dumps(interest_data)
    return render_template('dashboard/user-hobby.html', option=json.dumps(interest_data),
                           username=username, app_id=app_id, app_list=app_list)


@dashboard_bp.route('/dashboard/marriage')
def marriage():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
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


@dashboard_bp.route('/dashboard/consumption')
def consumption():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
        static_info = fake_data.get('static_info')
        consumption_obj = static_info.get('consumption')
        hascar_obj = static_info.get('has_car')
        haspet_obj = static_info.get('has_pet')
        consum = {'category': map(lambda x: translate(x, 'consumption'), consumption_obj.keys()),
                  'series': map(lambda x: consumption_obj.get(x), consumption_obj.keys())}
        car = {'category': map(lambda x: translate(x, 'has_car'), hascar_obj.keys()),
               'series': map(lambda x: hascar_obj.get(x), hascar_obj.keys())}
        pet = {'category': map(lambda x: translate(x, 'has_pet'), haspet_obj.keys()),
               'series': map(lambda x: haspet_obj.get(x), haspet_obj.keys())}
    else:
        result_dict = get_query_list(app_id, 'consumption', 'has_car', 'has_pet')
        consumption_list = filter(lambda x: x is not None, result_dict['consumption'])
        car_list = filter(lambda x: x is not None, result_dict['has_car'])
        pet_list = filter(lambda x: x is not None, result_dict['has_pet'])
        consumption_tmp = map(lambda x: list(x),
                              zip(*map(lambda x: [x, consumption_list.count(x)], set(consumption_list))))
        consum = {"category": map(lambda x: translate(x, 'consumption'), consumption_tmp[0]),
                  "series": consumption_tmp[1]} if consumption_tmp else {}
        car = {'category': map(lambda x: translate(x, 'has_car'), list(set(car_list))),
               'series': map(lambda x: car_list.count(x), list(set(car_list)))}
        pet = {'category': map(lambda x: translate(x, 'has_pet'), list(set(pet_list))),
               'series': map(lambda x: pet_list.count(x), list(set(pet_list)))}

    ret_json = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'consumption': consum,
            'car': car,
            'pet': pet
        }
    }
    return render_template('dashboard/user-consumption.html', option=json.dumps(ret_json),
                           username=username, app_id=app_id, app_list=app_list)


@dashboard_bp.route('/dashboard/location')
def location():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    result_dict = get_query_list(app_id, 'province', 'city')
    provice_list = map(lambda y: y if y[-1] not in ['省', '市'] else y[0:-1],
                       filter(lambda x: x is not None, result_dict['province']))
    city_list = filter(lambda x: x is not None, result_dict['city'])

    province = map(lambda x: {'name': x[0], 'value': x[1]},
                   sorted(map(lambda x: (x, provice_list.count(x)), set(provice_list)), key=lambda x: -x[1]))
    city = map(lambda x: {'name': x[0], 'value': x[1]},
               sorted(map(lambda x: (x, city_list.count(x)), set(city_list)), key=lambda x: -x[1]))
    location = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': {
            'province': province[:6],
            'city': city[:6]
        }
    }
    return render_template('dashboard/user-location.html', option=json.dumps(location),
                           app_id=app_id, app_list=app_list, username=username)


@dashboard_bp.route('/dashboard/context', methods=['GET', 'POST'])
def motion():
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

    s = json.load(file(join(dirname(dirname(__file__)), 'translate.json')))
    home_office_type = s.get('home_office_status').keys()

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
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
    return render_template('dashboard/scene.html', option=json.dumps(context),
                           username=username, app_id=app_id, app_list=app_list)


@dashboard_bp.route('/dashboard/single', methods=['GET', 'POST'])
def single():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    developer = Developer()
    developer.session_token = session.get('session_token')
    if request.method == 'POST':
        req_type = request.json.get('type')
        group_id = request.json.get('gourpid')

        if req_type == 'user_list':
            return json.dumps({"userNames": get_tracker_of_app(app_id, group_id=group_id)})

        uid = request.json.get('uid')
        h_start = request.json.get('h_start')
        h_end = request.json.get('h_end')
        e_start = request.json.get('e_start')
        e_end = request.json.get('e_end')
        workday = request.json.get('workday')
        ret_dict = get_attr_of_user(uid, h_start=h_start, h_end=h_end,
                                    e_start=e_start, e_end=e_end, workday=workday == 'workday')
        return dumps(ret_dict)
    return render_template('dashboard/single-user-motion.html',
                           username=username, app_id=app_id, app_list=app_list)


@dashboard_bp.route('/dashboard/group', methods=['GET', 'POST'])
def group():
    if not session.get('session_token'):
        next_url = '/dashboard/group'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()
    # tracker_list = developer.get_tracker_of_app(app_id)

    if request.method == 'POST':
        req_type = request.json.get('action')
        if req_type == 'group_list':
            return json.dumps({'group_list': get_groups()})
        elif req_type == 'update':
            args = dict(filter(lambda y: y[0] != 'action' and y[0] != 'id' and y[0] != 'name', dict(request.json).items()))
            args['id'] = request.json.get('id')
            args['name'] = request.json.get('name')
            create_group(args)
            flash("Update group info success!", 'msg')
            return redirect(url_for('dashboard_bp.group'))
        elif req_type == 'delete':
            group_id = request.json.get('id')
            delete_group(group_id)
            flash("Delete group info success!", 'msg')
            return redirect(url_for('dashboard_bp.group'))
        elif req_type == 'label_list':
            return json.dumps(get_label_list())
        else:
            return make_response("invalid action type!")
    return render_template('dashboard/group-setting.html', username=username,
                           app_id=app_id, app_list=app_list)


@dashboard_bp.route('/dashboard/push', methods=['GET', 'POST'])
def push():
    if not session.get('session_token'):
        next_url = '/dashboard/push'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    user_id = developer.user_id()
    app_list = developer.get_app_list()
    tracker_list = developer.get_tracker_of_app(app_id)
    if request.method == "POST":
        data = request.json
        data['devId'] = user_id
        data['appId'] = app_id
        url = "http://api.trysenz.com/notifyStrategy/createStrategy"
        rep = post_data(url=url, data=data)
        return make_response(json.dumps(rep))
    return render_template("dashboard/push-notification.html", username=username,
                           app_id=app_id, app_list=app_list, tracker_list=tracker_list)


@dashboard_bp.route('/dashboard/history', methods=['GET', 'POST'])
def history():
    if not session.get('session_token'):
        next_url = '/dashboard/push'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)
    if request.method == "POST":
        print request.json
    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()
    tracker_list = developer.get_tracker_of_app(app_id)
    return render_template('dashboard/push-notification-history.html', username=username,
                           app_id=app_id, app_list=app_list, tracker_list=tracker_list)


def create_group(args):
    group_id = args.get('id')
    query = Query(DashboardGroup)
    query.equal_to('objectId', group_id)
    group = query.first() if query.count() else DashboardGroup()
    group.clear()
    for k, v in args.items():
        group.set(k, v)
    group.save()


def delete_group(group_id):
    query = Query(DashboardGroup)
    query.equal_to('objectId', group_id)
    group = query.find()
    for item in group:
        item.destroy()


def get_groups():
    query = Query(DashboardGroup)
    groups = query.find()
    return map(lambda x: dict(x.attributes, id=x.id), groups)


def get_label_list():
    label = ['age', 'gender', 'marriage', 'pregnant', 'has_car',
             'has_pet', 'occupation', 'field', 'consumption', 'interest']
    f = file(join(dirname(dirname(__file__)), 'translate.json'))
    s = json.load(f)
    return map(lambda x: {"name": x, "data": s.get(x).keys()}, label)


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

    fake_data = json.load(file(join(dirname(dirname(__file__)), 'fake_data.json')))
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

    # TODO calc motion's duration

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
    home_addr = home.get("u_poi").get("poi_address") if home.get("u_poi") else ""
    office_addr = office.get("offices")[0].get("u_poi").get("poi_address") \
        if office.get("offices") and office.get("offices")[0].get("u_poi") else ""
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
        print x['level2_event']
        detail_data.append(x)
    ret_dict['detailData'] = detail_data
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




