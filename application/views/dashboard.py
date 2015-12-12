# coding: utf-8
from flask import Blueprint, render_template, json, session, request, make_response
from leancloud import Object, Query, LeanCloudError
from ..models import Developer
from os.path import dirname, join
import time

dashboard_bp = Blueprint('dashboard_bp', __name__, template_folder='templates')


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
    data = map(lambda x: {'rank': x/3+1, 'name': event_tmp[x-1][0]}, xrange(1, len(set(event_tmp))+1))
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

    print h_start, h_end, e_start, e_end, workday

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
    developer = Developer()
    developer.session_token = session.get('session_token')
    userNames = developer.get_tracker_of_app(app_id)
    userLabels = []
    return render_template('dashboard/single-user-motion.html')


def get_attr_of_user(uid):
    user = {
        "__type": "Pointer",
        "className": "_User",
        "objectId": uid
    }
    type_list = ['gender', 'age', 'field', 'occupation', 'interest',
                 'marriage', 'pregnant', 'consumption', 'has_car', 'has_pet']
    query = Query(Object.extend('DashboardSource'))
    query.equal_to('user', user)
    attrs = query.find()[0] if query.count() else {}

    for attr in type_list:
        attrs.attributes.get(attr)



def get_query_list(app_id='', *field):
    if not app_id:
        app_id = '5621fb0f60b27457e863fabb'

    app_query = Query(Object.extend('Application'))
    app_query.equal_to('app_id', app_id)
    app = app_query.find()[0] if app_query.count() else None

    try:
        query_limit = 100
        if app_id == '5621fb0f60b27457e863fabb':
            query = Query(Object.extend('DashDataSource'))
            query.equal_to('app_id', app_id)
        else:
            query = Query(Object.extend('DashboardSource'))
            query.equal_to('app', app)
        total_count = query.count()
        query_times = (total_count + query_limit - 1) / query_limit
        result_list = []
        for index in xrange(query_times):
            query.limit(query_limit)
            query.skip(index * query_limit)
            result_list.extend(query.find())
    except LeanCloudError:
        return {}
    # check all record in DashboardSource and ignore app_id simultaneous
    # select in front end
    if app_id == 'all':
        query = Query(Object.extend('DashboardSource'))
        total_count = query.count()
        query_times = (total_count + query_limit - 1) / query_limit
        result_list = []
        for index in xrange(query_times):
            query.limit(query_limit)
            query.skip(index * query_limit)
            result_list.extend(query.find())

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
                ret_dict[item] = map(lambda result: result.attributes.get(item, None), result_list)
    return ret_dict


def translate(target, arg):
    f = file(join(dirname(dirname(__file__)), 'translate.json'))
    s = json.load(f)
    return s.get(arg).get(target) or target


