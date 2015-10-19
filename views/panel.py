from flask import Blueprint, render_template
panel = Blueprint('panel', __name__, template_folder='templates')


@panel.route('/panel')
def show():
    return render_template('panel/test.html')


