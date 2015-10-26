from leancloud import User, Object, Query, LeanCloudError


class Developer:
    def __init__(self, user_id=None):
        self.user = User()
        self.user_id = user_id
        self.session_token = None
        self.tracker_list = []

    @classmethod
    def is_valid_emali(cls, email):
        query = Query(User)
        query.contained_in('email', email)
        return False if query.find() else True

    def signup(self, username, password, email=None):
        self.user.set('username', username)
        self.user.set('password', password)
        self.user.set('email', email)
        self.user.set('type', 'developer')
        return self.user.sign_up()

    def login(self, username, password):
        try:
            self.user.login(username, password)
            self.user_id = self.user.id
            self.session_token = self.user.get_session_token()
            return True
        except LeanCloudError:
            return False

    def logout(self, username):
        pass

    def get_tracker_of_app(self, app_id):
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
        user_set = set()
        for installation in installation_list:
            user_set.add(installation.attributes['user'].id)
        self.tracker_list = list(user_set)

