import time
import json
import requests
from os.path import dirname, join
from leancloud import Query, Object

Installation = Object.extend('BindingInstallation')
User = Object.extend('User')

user_to_installation = {}


def get_installationid_by_trackerid(tracker_id=None):
    print "tracker_id", tracker_id
    if not user_to_installation.get(tracker_id):
        query = Query(Installation)
        user = {
            "__type": "Pointer",
            "className": "_User",
            "objectId": tracker_id
        }
        query.equal_to('user', user)
        query.descending('updatedAt')
        print "query.count", query.count()
        installation = query.find()[0] if query.count() else {}
        print "query Installaton", installation.id
        user_to_installation[tracker_id] = [installation.id, installation.get('deviceType')]
    return user_to_installation.get(tracker_id)


def push_ios_message(installation_id, content_type, value, timestamp, source=None):
    url = "https://leancloud.cn/1.1/functions/pushAPNMessage"
    headers = {
        "Content-Type": "application/json",
        "X-AVOSCloud-Application-Id": "9ra69chz8rbbl77mlplnl4l2pxyaclm612khhytztl8b1f9o",
        "X-AVOSCloud-Application-Key": "1zohz2ihxp9dhqamhfpeaer8nh1ewqd9uephe9ztvkka544b"
    }
    body = {
        "type": content_type,
        "status": value,
        "timestamp": timestamp,
        "probability": 1,
        "source": source or "",
        "installationId": installation_id
    }
    print "push_ios_message", body
    rep = requests.post(url, headers=headers, data=json.dumps(body))
    print "push_ios_message", rep, rep.content


def push_android_message(uid, feature, value, timestamp, expire=None, source=None):
    url = "https://leancloud.cn/1.1/functions/notify_new_details"
    headers = {
        "Content-Type": "application/json",
        "X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
        "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"
    }
    body = {
        "type": feature,
        "val": value,
        "timestamp": timestamp,
        "userId": uid,
        "source": source or "",
        "expire": expire or ""
    }
    print "push_android_message", body
    rep = requests.post(url, headers=headers, data=json.dumps(body))
    print "push_android_message", rep, rep.content


def post_panel_data(**param):
    tracker = param.get('tracker')
    tracker_list = param.get('tracker_list')
    source = param.get('source') or ""
    timestamp = param.get('timestamp') or int(time.time()*1000)
    feature = param.get('type')
    value = param.get('value')

    if tracker != 'all':
        tracker_list = [tracker]
    for uid in tracker_list:
        if feature and value:
            installation = get_installationid_by_trackerid(uid)
            print "installation", installation
            if installation[1] == u'ios':
                push_ios_message(installation[0], feature, value, timestamp, source=source)
            push_android_message(uid, feature, value, timestamp, source=source)


def translate(target, arg):
    f = file(join(dirname(dirname(__file__)), 'translate.json'))
    s = json.load(f)
    return s.get(arg).get(target) or target


if __name__ == '__main__':
    # msg = {'source': '', 'type': 'motion', 'userId': u'5624d68460b2b199f7628914',
    #        'val': u'motionWalking', 'timestamp': 1453032377975}
    # push_android_message(msg.get('userId'), "motion", msg.get("val"), msg.get("timestamp"))
    msg = {'status': u'contextAtHome', 'probability': 1, 'timestamp': 1452848189611, 'source': '',
           'installationId': u'4Y5KKBtB7TuPrAiQd14xE1EarhJu0EQ0', 'type': 'home_office_status'}
    push_ios_message(msg.get("installationId"), msg.get("type"), msg.get("status"), msg.get("timestamp"))



