from leancloud import Query, Object
import leancloud

DashboardSource = Object.extend('DashboardSource')


def move():
    tb = Query(DashboardSource)
    tb.limit(1000)
    records = tb.find()
    count = 0
    for r in records:
        print r.id
        print count
        count += 1
        tmp = {}
        motion = r.attributes.get('motion') or {}
        for k, v in motion.items():
            if isinstance(v, unicode):
                tmp[k] = v
            if isinstance(v, dict):
                tmp[k] = v.values()[0]
        r.set('motion', tmp)
        r.save()


if __name__ == '__main__':
    leancloud.init('2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo',
                   '3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll')
    move()
