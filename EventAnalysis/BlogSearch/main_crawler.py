# coding=utf-8

import sys

# sys.path.append('home/yc/PycharmProjects/yqproject/yqproject/settings.py')
from MoblieWeibo import *
from start_search import *
from db_connection import *

__author__ = 'gu'
"""
7.27
测试完毕
"""

def run(event_list):
    """
        :return:
    """

    # MoblieWeibo().login('1939777358@qq.com', '123456a')
    # '70705420yc@sina.com', '1234567') ('meilanyiyou419@163.com','aaa333') 'odlmyfbw@sina.cn','tttt5555'
    serach_list(event_list)


def main_weibo(event_list,eid):

    """
        :return:
    """
    db = Database()
    now = datetime.datetime.now()
    run(event_list)
    end = datetime.datetime.now()
    npfoe = []  # news path for one event
    for key, values in result_dict.items():
        print key
        print '***********_____________***^^^^^^^^^^^^^^'
        for value in values:
            print value
        # [blog_id,content,originator,originator_id,post_time,topic,like_num,repost_num,comment_num,total_dir])
        db.save_news(values[0],eid,values[2],values[4],values[5],values[1],values[8],values[7],values[6])
        npfoe.append(values[9])
    print 'paths',npfoe
    print "用时: ", end - now
    return npfoe

# main_weibo(["王毅：奉劝日方不要一错再错，没完没了"])
