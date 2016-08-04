# coding=utf-8
__author__ = 'yc'

import redis
import redis.exceptions
import multiprocessing as mul

from EventAnalysis.BlogSearch.main_crawler import *
from EventDectection.EventDection import *
from KeyExtract.key_extract import *
from EventAnalysis.links_labels import *
from db_connection import *
from EventAnalysis.info import *
from Emotion.e1 import *
from EventAnalysis.info.attempt_three import *


def discover_path():
    """
    爬虫生成文件夹后,查找所有文件夹的路径,便于查找txt和xls文件
    :return: 事件文件夹路径列表
    """
    path_list = []
    for path, folders, files in os.walk(DOC_DIR):
        if files.__len__() != 0:
            path_list.append(path)
    return path_list


if __name__ == '__main__':
    db = Database()
    # r = redis.Redis(password='uliuli520')
    # pipe = r.pipeline()
    events = detect_event()  # [[list]]
    # for unit in events:
    #     pipe.rpush('title_list', unit[0])
    # a = pipe.lrange('title_list', 0, -1)
    # print pipe.execute()
    # print a
    for event in events:
        s = ''
        keyword_list = main_keyword(event)
        for i in keyword_list:
            s += i
            s += ','
        event_id = db.check_keyword(keyword_list)
        if event_id is None:
            event_id = db.save_events(event[0], s, 'null')
        else:
            pass
        main_weibo(event, event_id)
        path = 
        # path_list = discover_path()
        # for path in path_list:
            main_network(path)  # 网络图
            main_info(path)  # 年龄,地图
            main_emotion(path)  # 情绪图
            info_path = path.split('/',4)[4]
            db.update_event(event_id,info_path)



            # pool=mul.Pool(processes=2)
            # run=[main_network(),main_weibo()]
