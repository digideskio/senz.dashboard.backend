# coding: utf-8

from leancloud import User, Object, Query, LeanCloudError
from itsdangerous import Signer

Application = Object.extend('Application')
Installation = Object.extend('BindingInstallation')


class Developer(User):
    def __init__(self):
        self.tracker_list = []
        self.app_list = []
        self.app_dict = {}
        self.session_token = None
        User.__init__(self)

    def username(self):
        if self.session_token:
            return self.become(session_token=self.session_token).get_username()
        else:
            return None

    def user_id(self):
        if self.session_token:
            return self.become(session_token=self.session_token).id
        else:
            return None

    def create_new_app(self, app_name, app_type=None):
        if not app_name:
            return False
        user = self.become(session_token=self.session_token)
        app = Application()
        query = Query(Application)
        query.equal_to('user', user)
        query.equal_to('app_name', app_name)
        if not query.count():
            app.set('app_name', app_name)
            app.set('type', app_type)
            app.set('user', user)
            app.save()
            app_id = app.id
            signer = Signer('this is senz dashboard')
            app_key = (signer.sign(app_id).split(app_id + '.'))[1]
            app.set('app_id', app_id)
            app.set('app_key', app_key)
            app.save()
            return app_name, app_key, app_id
        return None

    def delete_app(self, app_id=None):
        try:
            user = self.become(session_token=self.session_token)
            query = Query(Application)
            query.equal_to('user', user)
            query.equal_to('app_id', app_id)
            result = query.find()
            if result:
                result[0].destroy()
                return True
            else:
                return False
        except LeanCloudError:
            return False

    def modify_app(self, app_id=None, app_name=None, app_type=None):
        try:
            user = self.become(session_token=self.session_token)
            query = Query(Application)
            query.equal_to('user', user)
            query.equal_to('app_id', app_id)
            app = query.find()[0] if query.count() else None
            if app:
                if app_name:
                    app.set('app_name', app_name)
                if app_type:
                    app.set('type', app_type)
                app.save()
                return True
            return False
        except LeanCloudError:
            return False

    def get_app_list(self):
        try:
            user = self.become(session_token=self.session_token)
            query = Query(Application)
            query.equal_to('user', user)
            query.limit(1000)
            result = query.find()
        except LeanCloudError:
            return []

        self.app_list = map(lambda x: {'app_id': x.attributes.get('app_id'),
                                       'app_key': x.attributes.get('app_key'),
                                       'app_type': x.attributes.get('type'),
                                       'createdAt': x.created_at.strftime("%Y-%m-%d"),
                                       'app_name': x.attributes.get('app_name')}, result)
        return self.app_list

    def get_tracker_of_app(self, app_id=''):
        try:
            the_app = {
                "__type": "Pointer",
                "className": "Application",
                "objectId": app_id
            }

            query = Query(Installation)
            query.equal_to('application', the_app)
            query.select('user')
            installation_list = query.find()
        except LeanCloudError:
            return []
        if not installation_list:
            self.tracker_list = []
        else:
            self.tracker_list = sorted(list(set(map(lambda x: x.attributes['user'].id, installation_list))))
        return self.tracker_list

Developer._class_name = '_User'





