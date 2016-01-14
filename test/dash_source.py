# coding: utf-8
from datetime import datetime
import leancloud
from leancloud import Object, Query
import redis
import json


def get_log_data():
    leancloud.init("9ra69chz8rbbl77mlplnl4l2pxyaclm612khhytztl8b1f9o",
                   "1zohz2ihxp9dhqamhfpeaer8nh1ewqd9uephe9ztvkka544b")
    start = datetime(2016, 1, 13)
    end = datetime(2016, 1, 14)
    query = Query(Object.extend('Log'))
    query.equal_to("type", "location")
    query.greater_than("createdAt", start)
    query.less_than("createdAt", end)

    # query_limit = 100
    # total_count = query.count()
    # query_times = (total_count + query_limit - 1) / query_limit
    result_list = query.find()
    # for index in xrange(query_times):
    #     query.limit(query_limit)
    #     query.skip(index * query_limit)
    #     result_list.extend(query.find())
    # print result_list[1].id
    # print "###################"
    # a = json.dumps(result_list[1])
    # print type(a)
    # print a
    return result_list


def connect_redis(obj):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('tttttt', obj)
    print r


if __name__ == "__main__":
    result_list = get_log_data()
    print (result_list[1])
    connect_redis(result_list[1])


