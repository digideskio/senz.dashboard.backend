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
        "installationId": installation_id
    }
    print "push_ios_message", body
    rep = requests.post(url, headers=headers, data=json.dumps(body))
    print type(rep), rep, rep.status_code, rep.content


def post_panel_data(**param):
    tracker = param.get('tracker')
    tracker_list = param.get('tracker_list')
    motion_type = param.get('motion_type') or ""
    motion_val = param.get('motion_val') or ""
    context_type = param.get('context_type') or ""
    context_val = param.get('context_val') or ""
    source = param.get('source') or ""
    timestamp = param.get('timestamp') or int(time.time()*1000)
    expire = param.get('expire')

    s = json.load(file(join(dirname(dirname(__file__)), 'translate.json')))
    home_office_type = s.get("home_office_status").keys() + s.get("home_office_status_old").keys()

    if tracker != 'all':
        tracker_list = [tracker]
    headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
               "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}
    for item in tracker_list:
        installation = get_installationid_by_trackerid(item)
        print "installation", installation
        payload = {"userId": item, "source": source, "timestamp": timestamp}
        if motion_type and motion_val:
            payload["type"] = motion_type
            payload["val"] = motion_val
            if installation[1] == u'ios':
                push_ios_message(installation[0], motion_type, motion_val, timestamp, source=source)
            rep = requests.post("https://leancloud.cn/1.1/functions/notify_new_details",
                                headers=headers, data=payload)
            print "motion", rep, rep.status_code, rep.content
        if context_type and context_val and context_type in home_office_type:
            payload["type"] = "home_office_status"
            payload["val"] = context_val
            payload["expire"] = expire
            if installation[1] == u'ios':
                push_ios_message(installation[0], "home_office_status", context_val, timestamp, source=source)
            rep = requests.post("https://leancloud.cn/1.1/functions/notify_new_details",
                                headers=headers, data=payload)
            print "home_office_status", rep, rep.status_code, rep.content
        elif context_type and context_val and context_type not in home_office_type:
            payload["type"] = "event"
            payload["val"] = context_val
            if installation[1] == u'ios':
                push_ios_message(installation[0], "event", context_val, timestamp, source=source)
            rep = requests.post("https://leancloud.cn/1.1/functions/notify_new_details",
                                headers=headers, data=payload)
            print "event", rep, rep.status_code, rep.content
        print "payload", payload


def translate(target, arg):
    f = file(join(dirname(dirname(__file__)), 'translate.json'))
    s = json.load(f)
    return s.get(arg).get(target) or target


if __name__ == '__main__':
    msg = {'status': u'contextAtHome', 'probability': 1, 'timestamp': 1452848189611, 'source': '',
           'installationId': u'ntK466fF6qCfJeYLwGYJ8od5L8n1gwXD', 'type': 'home_office_status'}
    push_ios_message(msg.get("installationId"), msg.get("type"), msg.get("status"), msg.get("timestamp"))


if __name__ == '__main__':
    msg = {
        "status": "contextAtWork",
        "probability": 1,
        "timestamp": 1452876156178,
        "source": "",
        "installationId": "4Y5KKBtB7TuPrAiQd14xE1EarhJu0EQ0",
        "type": "home_office_status"
    }
    push_ios_message(msg.get("installationId"),
                     msg.get("type"),
                     msg.get("status"),
                     msg.get("timestamp"))

