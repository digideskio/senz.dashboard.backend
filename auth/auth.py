# -*- Encoding: utf-8 -*-
from flask.ext.login import LoginManager
from leancloud import Object, Query
from server import app


login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(userid):
    query = Query(Object.extend('User'))
    query.equal_to('objectId', userid)
    return query.find()[0] if query.count() else None
