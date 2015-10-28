from models import Developer
from flask import Blueprint, render_template, session
integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    app_id = session.get('app_id', None)
    app_list = []
    if session.get('session_token'):
        app_list = session.get('app_list', None)
        if not app_list:
            developer = Developer()
            developer.session_token = session.get('session_token')
            app_list = developer.get_app_list()
            session['app_list'] = app_list
    return render_template('integration/integration.html',
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)

