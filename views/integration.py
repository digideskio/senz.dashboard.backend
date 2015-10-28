from models import Developer
from flask import Blueprint, render_template, session
integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    user = Developer()
    user.session_token = session.get('session_token')
    user.get_app_list()
    return render_template('integration/integration.html',
                           username=session.get('username'),
                           app_list=user.app_list)

