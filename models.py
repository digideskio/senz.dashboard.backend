# coding: utf-8

from leancloud import User, Object, Query, LeanCloudError
from itsdangerous import Signer


class Developer(User):
    def __init__(self):
        self.tracker_list = []
        self.app_list = []
        self.app_dict = {}
        self.session_token = None
        User.__init__(self)

    def login(self, username=None, password=None):
        User.login(self, username, password)
        self.session_token = self.get_session_token()
        if self.session_token:
            user = self.become(session_token=self.session_token)
            query = Query(Object.extend('Application'))
            query.equal_to('user', user)
            query.limit(1000)
            result = query.find()
            if result:
                self.app_list = map(lambda x: {'app_id': x.attributes['app_id'],
                                               'app_key': x.attributes['app_key'],
                                               'app_name': x.attributes['app_name']}, result)
                return True
        return False

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

    def get_app_list(self):
        try:
            user = self.become(session_token=self.session_token)
            query = Query(Object.extend('Application'))
            query.equal_to('user', user)
            query.limit(1000)
            result = query.find()
        except LeanCloudError, e:
            print(e)
            return []

        self.app_list = map(lambda x: {'app_id': x.attributes['app_id'],
                                       'app_key': x.attributes['app_key'],
                                       'app_name': x.attributes['app_name']}, result)
        return self.app_list

    def get_tracker_of_app(self, app_id=''):
        try:
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
        except LookupError, e:
            print(e)
            return []
        if not installation_list:
            self.tracker_list = []
        else:
            self.tracker_list = list(set(map(lambda x: x.attributes['user'].id, installation_list)))
        return self.tracker_list

Developer._class_name = '_User'





