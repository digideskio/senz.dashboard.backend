from leancloud import init
import requests
from create_fake_data import get_userid_list


def post_panel_data(**param):
    user_id = param.get('user_id')
    config = param.get('config')

    headers = {"X-AVOSCloud-Application-Id": "wsbz6p3ouef94ubvsdqk2jfty769wkyed3qsry5hebi2va2h",
               "X-AVOSCloud-Application-Key": "6z6n0w3dopxmt32oi2eam2dt0orh8rxnqc8lgpf2hqnar4tr"}

    payload = {"userId": user_id, "config": config}
    print(payload)
    rep = requests.post("https://leancloud.cn/1.1/functions/notify_new_config",  headers=headers, json=payload)
    print(rep.content)

if __name__ == '__main__':
    init('2x27tso41inyau4rkgdqts0mrao1n6rq1wfd6644vdrz2qfo',
         '3fuabth1ar3sott9sgxy4sf8uq31c9x8bykugv3zh7eam5ll')

    # user_id = "55b3ccd940ac21f9f969680a"
    tracker_list = get_userid_list()
    config = {
        "sensor": {
            "collector": {
                "isActive": True,
                "period": 30
            },
            "uploader": {
                "isActive": True,
                "strategy": "network",
                "period": 30
            }
        },
        "location": {
            "collector": {
                "isActive": True,
                "period": 30
            },
            "uploader": {
                "isActive": True,
                "strategy": "network",
                "period": 30
            }
        },
        "sound": {
            "collector": {
                "isActive": False,
                "period": 30
            },
            "uploader": {
                "isActive": False,
                "strategy": "wifi",
                "period": 30
            }
        },
        "calendar": {
            "collector": {
                "isActive": True,
                "period": 30
            },
            "uploader": {
                "isActive": True,
                "strategy": "wifi",
                "period": 30
            }
        }
    }

    for user_id in tracker_list:
        print(user_id)
        post_panel_data(user_id=user_id, config=config)
