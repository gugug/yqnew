# coding=utf-8

import sys
import os
from yqnew.settings import *

sys.path.append(os.path.join(BASE_DIR,'/yqnew/settings.py'))
# from MoblieWeibo import *
from start_search import *

__author__ = 'gu'
"""
7.27
测试完毕
"""

def run():
    """
        :return:
    """

    MoblieWeibo().login('1939777358@qq.com', '123456a')
    # '70705420yc@sina.com', '1234567') ('meilanyiyou419@163.com','aaa333') 'odlmyfbw@sina.cn','tttt5555'
    serach_list(["王毅：奉劝日方不要一错再错，没完没了"])


def main_weibo():

    """
        :return:
    """

    now = datetime.datetime.now()
    run()
    end = datetime.datetime.now()

    for key, values in result_dict.items():
        print key
        print '***********_____________***^^^^^^^^^^^^^^'
        for value in values:
            print value

    print "用时: ", end - now

main_weibo()
