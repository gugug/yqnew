# coding=utf-8
import datetime
import sched
import time
import os
# import redis

__author__ = 'gu'

s = sched.scheduler(time.time, time.sleep)
BASE_DIR = './'

def create_time_file():
    """
    生成时间
    :return:time_dir
    """
    try:
        now = datetime.datetime.now()
        other_style_time = now.strftime("%Y-%m-%d %H:%M")
        return other_style_time
    except:
        pass

def create_topic_file(topic, time_dir):
    """
    生成话题文件, 接上一个时间，
    :param: topic:
    :return:total_dir
    """
    try:
        total_dir = os.path.join(BASE_DIR, 'documents', 'topic', topic, time_dir)
        if os.path.exists(total_dir):
            print '语料目录已存在'
        else:
            os.makedirs(total_dir)
        return total_dir
    except:
        pass


