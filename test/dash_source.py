# coding: utf-8
import time
from datetime import date
import leancloud
from leancloud import Object, Query


if __name__ == '__main__':
    leancloud.init("2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo",
                   "3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll")
    uid = "564ee50600b0bf37d886519f"
    user = {
        "__type": "Pointer",
        "className": "_User",
        "objectId": uid
    }
    type_list = ['gender', 'age', 'field', 'occupation', 'interest',
                 'marriage', 'pregnant', 'consumption', 'has_car', 'has_pet']
    query = Query(Object.extend('DashboardSource'))
    query.equal_to('user', user)
    attrs = query.find()[0] if query.count() else {}
    Labels = filter(lambda y: y, map(lambda x: attrs.attributes.get(x), type_list)) if attrs else []
    userLabels = [y for x in Labels for y in x if isinstance(x, list)]
    #
    # query = Query(Object.extend('DashboardSource'))
    # query.limit(500)
    # results = query.find()
    # for res in results:
    #     events = res.attributes.get('event')
    #     if events is not None:
    #         events = dict(filter(lambda x: x[0] != 'null' and int(x[0]) >
    # time.time() - 24 * 3600 * 3, events.items()))
    #         print(events)
    #         for k, v in events.items():
    #             if isinstance(v, dict):
    #                 events[k] = v.get('event')
    #     print(events)
    #     print
    #     res.set('event', events)
    #     res.save()
    #
    # # print event_tmp
    # print date.strftime("%d-%m-%y")
