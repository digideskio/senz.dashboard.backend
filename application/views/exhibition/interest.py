from flask import render_template, Blueprint, request
from common import get_app_list, get_query_list
from application.common.util import translate
from os.path import dirname, join
import json

exhibition_interest = Blueprint('exhibition_interest', __name__, template_folder='templates')


@exhibition_interest.route('/dashboard/interest')
def show():
    context_dict = get_app_list()
    app_id = context_dict['app_id']
    username = context_dict['username']
    app_list = context_dict['app_list']

    if not app_id or app_id == '5621fb0f60b27457e863fabb':  # Demo App
        fake_data = json.load(file(join(dirname(dirname(dirname(__file__))), 'fake_data.json')))
        interest_obj = fake_data.get('interest')
        interest_tmp = interest_obj.items()
    else:
        result_dict = get_query_list(app_id, 'interest')
        interest_list = filter(lambda x: x is not None, result_dict['interest'])
        interest_tmp = [x for y in interest_list for x in y]
        interest_tmp = map(lambda x: (x, interest_tmp.count(x)), list(set(interest_tmp)))

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
