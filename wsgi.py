# -*- coding: utf-8 -*-

import os
import sys
import leancloud
from wsgiref import simple_server
from application.cloud import engine


APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

reload(sys)
sys.setdefaultencoding("utf-8")
leancloud.init(APP_ID, master_key=MASTER_KEY)
application = engine


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    #app.debug = True
    server = simple_server.make_server('localhost', PORT, application)
    print("Runing at http://localhost:%d" % PORT)
    server.serve_forever()
