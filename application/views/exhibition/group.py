# coding: utf-8
from flask import render_template, Blueprint, request, session, redirect, url_for, flash, make_response
from application.models import Developer
from leancloud import Object, Query
from os.path import dirname, join
import json

DashboardGroup = Object.extend('DashboardGroup')

exhibition_group = Blueprint('exhibition_group', __name__, template_folder='templates')


@exhibition_group.route('/dashboard/group', methods=['GET', 'POST'])
def show():
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
    print "@## group.show "
    return render_template('dashboard/group-setting.html', username=username,
                           app_id=app_id, app_list=app_list)


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
    f = file(join(dirname(dirname(dirname(__file__))), 'translate.json'))
    s = json.load(f)
    return map(lambda x: {"name": x, "data": s.get(x).keys()}, label)
