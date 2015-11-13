# coding: utf-8
import leancloud
from flask import json
from leancloud import Object
from os.path import dirname, join


if __name__ == '__main__':
    leancloud.init("llir9y4gtqys053tivb4tildoan0hgj87kdd0j6ib5naye5e",
                   "h5roibgrbtux2luasq1o9xwr218jebbsyuthv9ho4lced9rv")

    f = file(join(dirname(dirname(__file__)), 'application/translate.json'))
    s = json.load(f)
    print(s)

    config_tbl = Object.extend('Config')
    for k, v in s.items():
        print(k, v)
        config = config_tbl()
        config.set('name', k)
        config.set('value', v)
        config.save()

