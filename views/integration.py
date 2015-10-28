from models import Developer
from flask import Blueprint, render_template, session
integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    app_id = session.get('app_id', None)
    if 'app_list' in session:
        app_list = session.get('app_list')
    else:
        user = Developer()
        user.session_token = session.get('session_token')
        user.get_app_list()
        app_list = user.app_list
        session['app_list'] = app_list
    return render_template('integration/integration.html',
                           username=session.get('username'),
                           app_id=app_id,
                           app_list=app_list)

