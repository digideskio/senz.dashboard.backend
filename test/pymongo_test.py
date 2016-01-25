from pymongo import *
import requests
import datetime
import json
import time
import arrow


client = MongoClient('mongodb://senzhub:Senz2everyone@119.254.111.40/RefinedLog')
target = client.get_default_database().UserLocation

userEvent = client.get_default_database().UserEvent

# for i in userEvent.find({"type": "test"}):
#     print i.get("startTime"), i.get("createdAt")

yts0 = 1453334400
yts1 = 1453420800
y0 = datetime.datetime.utcfromtimestamp(yts0)
y1 = datetime.datetime.utcfromtimestamp(yts1)
# uids = ["5624d68460b2b199f7628914", "5684d3d660b2b60f65d84285", "569ccda100b04bbf1ee10b4a", "5684fa9e00b009a31af7efcb", "559f81fbe4b0ed48f0552737"]
uids = ['569e0eae2e958a0059d8ec1e']
for uid in uids[3:4]:
    print "UID: ", uid
    for i in target.find({"user_id": uid, "createdAt": {"$gt": y0, "$lt": y1}}).sort('timestamp', ASCENDING):
        timestamp = int(i.get("timestamp") or 0)
        createdAt = i.get("createdAt")

        ts_datetime_str = arrow.get(timestamp/1000).to('local').format()
        ct_str = arrow.get(createdAt).to("local").format()

        print timestamp, " ##Timestamp### ", ts_datetime_str, " ##CreatedAt## ", ct_str
    print "$$$$$$$$$$$$$$$$$$$$$$$$$"

# url = "http://0.0.0.0:3000/api/UserEvents"
# data = {
#     "test": str(datetime.datetime.fromtimestamp(1453279688))
# }
#
# print requests.post(url=url, json=json.dumps(data))

if __name__ == '__main__':
    # print datetime.datetime.utcfromtimestamp(yts0).isoformat()
    print datetime.datetime.isoformat(datetime.datetime.now())
    # print time.mktime((i for i in datetime.datetime.now()))


