from leancloud import init
import requests
import json


def post_panel_data(**param):
    user_id = param.get('user_id')
    config = param.get('config')

    headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
               "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}

    payload = {"userId": user_id, "config": config}
    rep = requests.post("http://leancloud.cn/1.1/functions/notify_new_config",  headers=headers, json=payload)
    print(rep.content)

if __name__ == '__main__':
    init('pin72fr1iaxb7sus6newp250a4pl2n5i36032ubrck4bej81',
         'qs4o5iiywp86eznvok4tmhul360jczk7y67qj0ywbcq35iia')

    user_id = "55b3ccd940ac21f9f969680a"
    config = {
        "period": 30,
        "collector": {
            "sensor": {
                "isActive": True
            },
            "location": {
                "isActive": True
            },
            "sound": {
                "isActive": False
            },
            "calendar": {
                "isActive": True
            }
        },
        "uploader": {
            "sensor": {
                "isActive": True,
                "strategy": "network"
            },
            "location": {
                "isActive": True,
                "strategy": "network"
            },
            "sound": {
                "isActive": False,
                "strategy": "wifi"
            },
            "calendar": {
                "isActive": True,
                "strategy": "wifi"
            }
        }
    }

    post_panel_data(user_id=user_id, config=config)
