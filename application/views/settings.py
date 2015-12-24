from flask import Blueprint, render_template, session, request, redirect, url_for, make_response, flash
from ..models import Developer
from leancloud import File
from StringIO import StringIO
from leancloud import Object, Query


settings = Blueprint('settings', __name__, template_folder='templates')
Application = Object.extend('Application')


@settings.route('/settings')
def show():
    if not session.get('session_token'):
        next_url = '/settings'
        return redirect(url_for('accounts_bp.login') + '?next=' + next_url)
    return redirect(url_for('settings.add_app'))


@settings.route('/create', methods=['GET', 'POST'])
def add_app():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))
    if request.method == 'GET':
        app_id = session.get('app_id', None)
        developer = Developer()
        developer.session_token = session.get('session_token')
        username = developer.username()
        app_list = developer.get_app_list()
        return render_template('settings/create.html',
                               username=username,
                               app_id=app_id,
                               app_list=app_list)
    if request.method == 'POST':
        app_name = request.form['app_name']
        app_type = request.form['app_type']
        user = Developer()
        user.session_token = session.get('session_token')
        app = user.create_new_app(app_name, app_type)
        if app:
            return render_template('settings/appkey.html',
                                   app_id=app[2],
                                   app_key=app[1])
        else:
            return redirect(url_for('settings.show'))


@settings.route('/manage', methods=['GET', 'POST'])
def manage_app():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))
    if request.method == 'GET':
        app_id = session.get('app_id', None)
        developer = Developer()
        developer.session_token = session.get('session_token')
        username = developer.username()
        app_list = developer.get_app_list()
        return render_template('settings/manage.html',
                               username=username,
                               app_id=app_id,
                               app_list=app_list)
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        if app_id is not '5621fb0f60b27457e863fabb' and app_id is not 'all':
            print "delete", '<', app_id, '>'
            user = Developer()
            user.session_token = session.get('session_token')
            user.delete_app(app_id)
        return redirect(url_for('settings.manage_app'))


@settings.route('/modify', methods=['POST'])
def modify_app():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        app_name = request.form.get('app_name')
        app_type = request.form.get('app_type')
        if app_id is not '5621fb0f60b27457e863fabb' and app_id is not 'all':
            print "modify", '<', app_id, '>'
            user = Developer()
            user.session_token = session.get('session_token')
            user.modify_app(app_id, app_name, app_type)
        return redirect(url_for('settings.manage_app'))


@settings.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('session_token'):
        return redirect(url_for('accounts_bp.login'))

    app_id = session.get('app_id', None)
    developer = Developer()
    developer.session_token = session.get('session_token')
    username = developer.username()
    app_list = developer.get_app_list()

    if request.method == "POST":
        cert = request.files.get('cert')
        key = request.files.get('key')
        app_id = request.form.get('appId')
        passphrase = request.form.get('passphrase')
        if app_id not in map(lambda x: x['app_id'], app_list):
            flash("This appId owned by others", "alert")
            return redirect(url_for("settings.upload"))

        cert_pem = File(app_id + '_cert.pem', StringIO(cert.read()))
        key_pem = File(app_id + '_key.pem', StringIO(key.read()))
        cert_pem.metadata.update(owner=username)
        key_pem.metadata.update(owner=username)
        cert_url = cert_pem.save().url
        key_url = key_pem.save().url

        app_query = Query(Application)
        app_query.equal_to('objectId', app_id)
        app = app_query.first()

        if app:
            app.set('cert_url', cert_url)
            app.set('key_url', key_url)
            app.set('passphrase', passphrase)
            app.save()
        flash("Certificate has added done!")
        return redirect(url_for("settings.upload"))
    return render_template('settings/upload.html', username=username,
                           app_id=app_id, app_list=app_list)
