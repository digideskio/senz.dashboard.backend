# coding: utf-8
from flask import Blueprint, render_template, jsonify

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show():
    return render_template('dashboard/test.html')


@dashboard.route('/dashboard/profile')
def profile():
    gender = {'category': ['male', 'female'], 'series': [209, 249]}
    age = {"category": ["55up", "35to55", "16to35", "16down"], "series": [209, 249, 299, 304]}
    job = {"category": ["工程师", "销售", "教师", "学生", "军人", "公务员", "管理人员", "自由职业", "其他"],
           "series": [12, 21, 10, 4, 12, 5, 6, 5, 2]}
    profession = {"category": ["IT", "贸易", "法律", "体育", "医务", "人力", "金融", "建筑", "人文科学", "自然科学", "制造业"],
                  "series": [12, 21, 10, 4, 12, 5, 6, 5, 2, 3, 1]}
    data = {'gender': gender, 'age': age, 'job': job, 'profession': profession}
    user_profile = {
        'errcode': 0,
        'errmsg': 'ok',
        'data': data
    }
    return jsonify(user_profile)


@dashboard.route('/dashboard/interest')
def interest():
    pass


@dashboard.route('/dashboard/marriage')
def marriage():
    pass


@dashboard.route('/dashboard/consumption')
def consumption():
    pass


@dashboard.route('/dashboard/location')
def location():
    pass
