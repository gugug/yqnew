# coding=utf-8
import datetime
import sched
import time
from yqnew.settings import *
__author__ = 'gu'

s = sched.scheduler(time.time, time.sleep)

def create_time_file():
    """
    生成时间目录，但没有创建
    :return:time_dir
    """
    try:
        now = datetime.datetime.now()
        other_style_time = now.strftime("%Y-%m-%d %H:%M")
        time_dir = os.path.join(BASE_DIR, 'documents', 'topic', str(other_style_time))
        return time_dir
    except:
        pass


def create_topic_file(time_dir,topic):
    """
    接上上一个时间目录，生成话题文件
    :param: topic:
    :return:total_dir
    """
    try:
        total_dir = time_dir + '/' + topic
        if os.path.exists(total_dir):
            print '语料目录已存在'
        else:
            os.makedirs(total_dir)
        return total_dir
    except:
        pass

# time_dir = create_time_file()
# create_topic_file(time_dir,"认同")