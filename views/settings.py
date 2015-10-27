from flask import Blueprint, render_template, session
settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/settings')
def show():
    return render_template('settings/settings.html', username=session.get('username'))

