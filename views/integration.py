from flask import Blueprint, render_template, session
integration = Blueprint('integration', __name__, template_folder='templates')


@integration.route('/integration')
def show():
    return render_template('integration/integration.html', username=session.get('username'))

