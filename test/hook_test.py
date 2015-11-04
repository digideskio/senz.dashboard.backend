from leancloud import Object, Query, init
import requests
import json

query_limit = 1000


def get_obj_list(obj_name):
    query = Query(Object.extend(obj_name))
    total_count = query.count()
    query_times = (total_count + query_limit - 1) / query_limit
    ret_list = []
    for index in range(query_times):
        query.limit(query_limit)
        query.skip(index * query_limit)
        ret_list.extend(query.find())
    return ret_list


if __name__ == '__main__':
    init('2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo',
         '3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll')
    headers = {"X-AVOSCloud-Application-Id": "2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo",
               "X-AVOSCloud-Application-Key": "3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll"}
    for t in get_obj_list('Test'):
        print(json.dumps(t.attributes))
        requests.post("http://localhost:3000/1.1/functions/test",  headers=headers, data=json.dumps(t.attributes))
