from pymongo import *

client = MongoClient('mongodb://senzhub:Senz2everyone@119.254.111.40/RefinedLog')
target = client.get_default_database().CombinedTimelines

for i in target.find({}):
    print i
