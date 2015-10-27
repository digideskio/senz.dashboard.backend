# coding: utf-8

from leancloud import User, Object, Query
from itsdangerous import Signer


class Developer(User):
    def __init__(self):
        self.tracker_list = []
        self.app_dict = {}
        self.session_token = None
        User.__init__(self)

    def user_id(self):
        if self.session_token:
            return self.become(session_token=self.session_token).id
        else:
            return None

    def create_new_app(self, app_name):
        if not app_name:
            return False
        user = self.become(session_token=self.session_token)
        application = Object.extend('Application')
        app = application()
        query = Query(application)
        query.equal_to('user', user)
        query.equal_to('app_name', app_name)
        if not query.find():
            app.set('app_name', app_name)
            app.set('user', user)
            app.save()
            app_id = app.id
            signer = Signer('this is senz dashboard')
            app_key = (signer.sign(app_id).split(app_id + '.'))[1]
            app.set('app_id', app_id)
            app.set('app_key', app_key)
            app.save()
            return True
        return False

    def delete_app(self, app_id=None):
        try:
            user = self.become(session_token=self.session_token)
            application = Object.extend('Application')
            query = Query(application)
            query.equal_to('user', user)
            query.equal_to('app_id', app_id)
            result = query.find()
            if result:
                result[0].destroy()
                return True
            else:
                return False
        except LookupError, e:
            print(e)
            return False

    def get_app_dict(self, user_id=''):
        query = Query(Object.extend('_User'))
        query.equal_to('objectId', user_id)
        if query.find():
            user = query.find()[0]
        else:
            self.app_dict = {}
            return {}
        query = Query(Object.extend('Application'))
        query.equal_to('user', user)
        query.limit(1000)
        app_list = query.find()
        if app_list:
            self.app_dict = dict(map(lambda x: (x.attributes['app_id'],
                                                {'app_name': x.attributes['app_name'],
                                                 'app_key': x.attributes['app_key']}), app_list))
        else:
            self.app_dict = {}
        return self.app_dict

    def get_tracker_of_app(self, app_id=''):
        query = Query(Object.extend('Application'))
        query.equal_to('app_id', app_id)
        app_list = query.find()
        if not app_list:
            return []
        the_app = app_list[0]

        query = Query(Object.extend('BindingInstallation'))
        query.equal_to('application', the_app)
        query.select('user')
        installation_list = query.find()
        self.tracker_list = list(set(map(lambda x: x.attributes['user'].id, installation_list)))

Developer._class_name = '_User'
