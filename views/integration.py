from models import Developer
from flask import Blueprint, render_template, session
integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    user = Developer()
    user.session_token = session.get('session_token')
    user_id = user.user_id()
    app_dict = user.get_app_dict(user_id)
    return render_template('integration/integration.html',
                           username=session.get('username'),
                           app_dict=app_dict)

