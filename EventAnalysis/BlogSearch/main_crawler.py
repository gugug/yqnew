# coding=utf-8

import sys

from db_connection import *

sys.path.append(os.path.join(BASE_DIR,'/yqnew/settings.py'))
# from MoblieWeibo import *
from start_search import *

__author__ = 'gu'
"""
7.27
测试完毕
"""

def run(title_list):
    """
        :return:
    """

    MoblieWeibo().login('1939777358@qq.com', '123456a')
    # '70705420yc@sina.com', '1234567') ('meilanyiyou419@163.com','aaa333') 'odlmyfbw@sina.cn','tttt5555'
    serach_list(title_list)


def main_weibo(title_list,eid):

    """
        :return:
    """
    db = Database()
    now = datetime.datetime.now()
    run(title_list)
    end = datetime.datetime.now()

    for key, values in result_dict.items():
        print key
        print '***********_____________***^^^^^^^^^^^^^^'
        for i in range(0,len(values)):
            print values[i]
        #     print "博文id ", blog_id
        # print "博文内容 ", content
        # print "发源者昵称 ", originator
        # print "发源者id ", originator_id
        # print "发表时间 ", post_time
        # print "话题 ", topic
        # print "点赞数 ", like_num
        # print "转发数 ", repost_num
        # print "评论数 ", comment_num
        #     db.save_news(values[0],eid,values[2],values[4],values[5],values[1],values[8],values[7],values[6])



    print "用时: ", end - now
    return
main_weibo(["【10名#游客在阿富汗遇袭身亡# 另有5人受伤】","【快讯：10名#游客在阿富汗遇袭身亡# 另有5人受伤】"],'111')
