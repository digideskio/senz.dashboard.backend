from pymongo import *
import requests
import datetime
import json

# client = MongoClient('mongodb://senzhub:Senz2everyone@119.254.111.40/RefinedLog')
# target = client.get_default_database().CombinedTimelines
#
# for i in target.find({}):
#     print i

url = "http://0.0.0.0:3000/api/UserEvents"
data = {
    "test": str(datetime.datetime.fromtimestamp(1453279688))
}

print requests.post(url=url, json=json.dumps(data))

