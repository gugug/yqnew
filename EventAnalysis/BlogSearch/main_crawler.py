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
    print 'run'
    search_list(event_list)


def main_weibo(event_list, eid):
    db = Database()
    now = datetime.datetime.now()
    run(event_list)
    while len(result_dict.values()) == 0:
        print "len_result_dict长度为0,需要休息60秒到120秒重跑"
        time.sleep(random.randint(30, 60))
        run(event_list)
    end = datetime.datetime.now()
    npfoe = []  # news path for one event

    print "len_result_dict", len(result_dict.values())

    for key, values in result_dict.items():
        print key
        print '***********_____________***^^^^^^^^^^^^^^'
        for value in values:
            print value

        # [blog_id,content,originator,originator_id,post_time,topic,like_num,repost_num,comment_num,total_dir])

        db.save_news(values[0], eid, values[2], values[4], values[5], values[1], values[8], values[7], values[6])
        npfoe.append(values[9])

    result_dict.clear()

    print 'paths', npfoe
    print "用时: ", end - now
    return npfoe

# main_weibo(["王毅：奉劝日方不要一错再错，没完没了"])
