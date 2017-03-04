# coding=utf-8
from Queue import Queue
import re

from yqnew.settings import *
from RedisQueue import RedisQueue

__author__ = 'gu'


def set_key(redis_key):
    """
    以事件为redis的key
    :param redis_key:事件
    :return:
    """
    global redis
    redis = RedisQueue(redis_key)


def read_txt(file_name):
    """
    打开文本，把对应的内容放进队列
    :param file_name: 文本所在的位置
    :return:
    """
    queue = Queue()
    txt = open(file_name, 'r')
    words = txt.readlines()
    for i in range(len(words)):
        words[i] = words[i].replace('\n', '')
        # print words[i]
        queue.put(words[i])
    os.remove(file_name)
    # print 'There are %d username' % queue.qsize()
    return queue


def get_file_list(dir, file_list):
    """
    获取事件参与人的绝对路径
    :param dir: 缩小范围查找的路径
    :param file_list: 绝对路径
    :return:
    """
    new_dir = dir
    if os.path.isfile(dir):
        file_list.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹
            if s == "repost_path.txt" or s == "comment.txt":
                continue
            new_dir = os.path.join(dir,s)
            get_file_list(new_dir, file_list)
    return file_list


def event_patn_dict():
    """
    一个事件对应着多个参与本文的绝对路径,此处是对应在topic1下的文件
    :return:
    """
    file_list = get_file_list(os.path.join(BASE_DIR, 'documents', 'topic'), [])
    event_pattern = re.compile('/topic/(.*?/.*?)/')
    patn_dict = {}
    for fl in file_list:
        patn_dict.setdefault(event_pattern.findall(fl)[0], []).append(fl)
    return patn_dict

def main_put():
    """
    把队列的内容放进redis
    :return:
    """
    patn_dict = event_patn_dict()
    for event_key, value in patn_dict.items():
        topic = re.split('/', event_key)
        set_key(topic[0])
        # print topic[0]
        # print value[0]  # 把最新检测时间下的参与人路径
        queue = read_txt(value[0])
        while not queue.empty():  # 如果队列不空
            username = queue.get()  # 取第一个然后移出
            redis.put(username)
        print 'There are %d username' % redis.qsize()

