from leancloud import Query, Object
from flask import Blueprint, request, make_response

dash_source = Blueprint('dash_source', __name__)


@dash_source.route('/v1/Location', methods=['POST'])
def update_location_info():
    user_id = request.json.get('user_id', None)
    if not user_id:
        return make_response('Error')
    location = request.json.get('location', None)
    update_info_leancloud(user_id, {'location': location})
    return make_response('OK')


@dash_source.route('/v1/Motion', methods=['POST'])
def update_motion_info():
    # motion: home_office_status
    user_id = request.json.get('user_id', None)
    if not user_id:
        return make_response('Error')
    home_office_status = request.json.get('home_office_status')
    update_info_leancloud(user_id, {'home_office_status': home_office_status})
    return make_response('OK')


@dash_source.route('/v1/Event', methods=['POST'])
def update_event_info():
    user_id = request.json.get('user_id', None)
    if not user_id:
        return make_response('Error')
    event = request.json.get('event', None)
    update_info_leancloud(user_id, {'event': event})
    return make_response('OK')


@dash_source.route('/v1/StaticInfo', methods=['POST'])
def update_static_info():
    user_id = request.json.get('user_id', None)
    if not user_id:
        return make_response('Error')
    staticInfo = request.json.get('staticInfo', None)
    parse_dict = parse_static_info(staticInfo=staticInfo)
    update_info_leancloud(user_id, parse_dict)
    return make_response('OK')


def update_info_leancloud(user_id, parse_dict):
    # get user Object
    query = Query(Object.extend('_User'))
    query.equal_to('objectId', user_id)
    user = query.find()[0]
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
        DashboardSource = Object.extend('DashboardSource')
        query = Query(DashboardSource)
        query.equal_to('app', app)
        query.equal_to('user', user)
        dst_table =query.find()
        if not dst_table:
            dst_table = DashboardSource()
        else:
            dst_table = dst_table[0]

        dst_table.set('app', app)
        dst_table.set('user', user)
        for key, value in parse_dict.items():
            if value:
                dst_table.set(key, value)
        dst_table.save()


def parse_static_info(staticInfo):
    ret_dict = {}
    age = ''
    if 'age' in staticInfo:
        age_dict = staticInfo.get('age')
        age = sorted(age_dict.items(), key=lambda age_dict: -age_dict[1])[0][0]
    ret_dict['age'] = age

    gender = '' if 'gender' not in staticInfo else 'male' if staticInfo.get('marriage') > 0 else 'female'
    ret_dict['gender'] = gender

    consumption = ''
    if consumption in staticInfo:
        consumption_dict = staticInfo.get('consumption')
        consumption = sorted(consumption_dict.items(), key=lambda consumption_dict: -consumption_dict[1])[0][0]
    ret_dict['consumption'] = consumption

    occupation = ''
    if 'occupation' in staticInfo:
        occupation_dict = staticInfo.get('occupation')
        occupation = sorted(occupation_dict.items(), key=lambda occupation_dict: -occupation_dict[1])[0][0]
    ret_dict['occupation'] = occupation

    field = ''
    if 'field' in staticInfo:
        field_dict = staticInfo.get('field')
        field = sorted(field_dict.items(), key=lambda field_dict: -field_dict[1])[0][0]
    ret_dict['field'] = field

    sport = ''
    if 'sport' in staticInfo:
        sport_dict = staticInfo.get('sport')
        sport = sorted(sport_dict.items(), key=lambda sport_dict: -sport_dict[1])[0][0]
    ret_dict['sport'] = sport

    marriage = '' if 'marriage' not in staticInfo else 'yes' if staticInfo.get('marriage') > 0 else 'no'
    ret_dict['marriage'] = marriage
    has_pet = '' if 'has_pet' not in staticInfo else 'yes' if staticInfo.get('has_pet') > 0 else 'no'
    ret_dict['has_pet'] = has_pet
    has_car = '' if 'has_car' not in staticInfo else 'yes' if staticInfo.get('has_car') > 0 else 'no'
    ret_dict['has_car'] = has_car
    pregnant = '' if 'pregnant' not in staticInfo else 'yes' if staticInfo.get('pregnant') > 0 else 'no'
    ret_dict['pregnant'] = pregnant
    social = '' if 'social' not in staticInfo else 'yes' if staticInfo.get('social') > 0 else 'no'
    ret_dict['social'] = social
    indoorsman = '' if 'indoorsman' not in staticInfo else 'yes' if staticInfo.get('indoorsman') > 0 else 'no'
    ret_dict['indoorsman'] = indoorsman
    acg = '' if 'acg' not in staticInfo else 'yes' if staticInfo.get('acg') > 0 else 'no'
    ret_dict['acg'] = acg
    tvseries_show = '' if 'tvseries_show' not in staticInfo else 'yes' if staticInfo.get('tvseries_show') > 0 else 'no'
    ret_dict['tvseries_show'] = tvseries_show
    variety_show = '' if 'variety_show' not in staticInfo else 'yes' if staticInfo.get('variety_show') > 0 else 'no'
    ret_dict['variety_show'] = variety_show
    game_show = '' if 'game_show' not in staticInfo else 'yes' if staticInfo.get('game_show') > 0 else 'no'
    ret_dict['game_show'] = game_show
    sports_show = '' if 'sports_show' not in staticInfo else 'yes' if staticInfo.get('sports_show') > 0 else 'no'
    ret_dict['sports_show'] = sports_show
    health = '' if 'health' not in staticInfo else 'yes' if staticInfo.get('health') > 0 else 'no'
    ret_dict['health'] = health
    gamer = '' if 'gamer' not in staticInfo else 'yes' if staticInfo.get('gamer') > 0 else 'no'
    ret_dict['gamer'] = gamer
    study = '' if 'study' not in staticInfo else 'yes' if staticInfo.get('study') > 0 else 'no'
    ret_dict['study'] = study
    game_news = '' if 'game_news' not in staticInfo else 'yes' if staticInfo.get('game_news') > 0 else 'no'
    ret_dict['game_news'] = game_news
    sports_news = '' if 'sports_news' not in staticInfo else 'yes' if staticInfo.get('sports_news') > 0 else 'no'
    ret_dict['sports_news'] = sports_news
    business_news = '' if 'business_news' not in staticInfo else 'yes' if staticInfo.get('business_news') > 0 else 'no'
    ret_dict['business_news'] = business_news
    current_news = '' if 'current_news' not in staticInfo else 'yes' if staticInfo.get('current_news') > 0 else 'no'
    ret_dict['current_news'] = current_news
    entertainment_news = '' if 'entertainment_news' not in staticInfo else 'yes' if staticInfo.get('entertainment_news') > 0 else 'no'
    ret_dict['entertainment_news'] = entertainment_news
    tech_news = '' if 'tech_news' not in staticInfo else 'yes' if staticInfo.get('tech_news') > 0 else 'no'
    ret_dict['tech_news'] = tech_news
    offline_shopping = '' if 'offline_shopping' not in staticInfo else 'yes' if staticInfo.get('offline_shopping') > 0 else 'no'
    ret_dict['offline_shopping'] = offline_shopping
    online_shopping = '' if 'online_shopping' not in staticInfo else 'yes' if staticInfo.get('online_shopping') > 0 else 'no'
    ret_dict['online_shopping'] = online_shopping
    return ret_dict
