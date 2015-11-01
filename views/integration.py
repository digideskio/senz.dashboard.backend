from models import Developer
from flask import Blueprint, render_template, session, redirect, url_for

integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    # app_list = server.cache.get('app_list')
    # if not app_list:
    app_list = developer.get_app_list()
    # server.cache.set('app_list', app_list)
    return render_template('integration/integration.html',
                           username=username,
                           app_id=app_id,
                           app_list=app_list)

