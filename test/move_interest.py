import leancloud
from flask import json
from os.path import dirname, join
from leancloud import Object, Query
from create_fake_data import get_tracker_of_app


src_list = []
dst = 'interest'


if __name__ == '__main__':
    leancloud.init('2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo',
                   '3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll')
    query = Query(Object.extend('UserInfoLog'))
    query.limit(1000)
    staticInfo_list = map(lambda x: x.attributes.get('staticInfo'), query.find())
    translation = json.load(file(join(dirname(dirname(__file__)), 'application/translate.json')))

    interest_dict = {}
    for result in query.find():
        interest = []
        uid = result.attributes.get('user').id
        interest_dict[uid] = []
        staticInfo = result.attributes.get('staticInfo')
        # print staticInfo
        for key, value in staticInfo.items():
            if key == 'sport':
                interest += value.keys()
            if key in translation.get('interest').keys():
                interest.append(key)
        interest_dict[uid] += interest

    uid_list = map(lambda x: x.attributes.get('user').id, query.find())
    print len(set(uid_list))
    for uid in set(uid_list):
        print uid
        user_query = Query(Object.extend('_User'))
        user_query.equal_to('objectId', uid)
        user = user_query.find()[0] if user_query.count() else None

        query = Query(Object.extend('DashboardSource'))
        query.equal_to('user', user)
        target_obj = query.find()[0]
        print interest_dict[uid]
        target_obj.set('interest', interest_dict[uid])
        target_obj.save()


