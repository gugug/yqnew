# coding=utf-8
__author__ = 'yc'

# import redis
# import redis.exceptions
import multiprocessing as mul

from EventAnalysis.BlogSearch.main_crawler import *
from EventDectection.EventDection import *
from KeyExtract.key_extract import *
from EventAnalysis.links_labels import *
from db_connection import *
from EventAnalysis.info import *
from Emotion.e1 import *
from EventAnalysis.info.attempt_three import *


def aggregate(path_list):
    """
    把属于同一个事件的新闻数据聚合起来
    :param path_list: 同事件的新闻文件夹路径
    :return:
    """
    split_path = path_list[0].split('/')
    event = split_path[3]
    time = split_path[5]
    all_path = os.path.join(event,time)
    folder_path = os.path.join(DOC_DIR,all_path)
    if os.path.exists(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    all_cmt = open(os.path.join(DOC_DIR,all_path,'comment.txt'),'a+')
    all_par = open(os.path.join(DOC_DIR,all_path,'participants.txt'),'a+')
    all_rpt = open(os.path.join(DOC_DIR,all_path,'repost_path.txt'),'a+')
    for path in path_list:
        cmt_file = open(os.path.join(path,'comment.txt'),'r')
        all_cmt.writelines(cmt_file.readlines())
        cmt_file.close()

        par_file = open(os.path.join(path,'participants.txt'),'r')
        all_par.writelines(par_file.readlines())
        par_file.close()

        rpt_file = open(os.path.join(path,'repost_path.txt'),'r')
        all_rpt.writelines(rpt_file.readlines())
        rpt_file.close()

    all_rpt.close()
    all_par.close()
    all_cmt.close()
    return all_path

# def get_news_path():
#     """
#     从redis中获取同一个事件的新闻的文件路径列表
#     :return:
#     """
#     rd = redis.Redis(password='uliuli520')
#     path_list = rd.lrange('npfoe',0,-1)
#     rd.delete('npfoe')
#     return path_list


def main():
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
        if event_id is None: # first time detected
            event_id = db.save_events(event[0], s, 'null')
            path_list = main_weibo(event, event_id) # redis get news paths for one event
            # ./documents/topic/【怪我不够好】/【就慢一点点，孙杨不哭！】/2016-08-07 19:52
            event_path = aggregate(path_list)
            db.update_event(event_id,event_path)
            main_info(os.path.join(DOC_DIR,event_path))  # 年龄,地图
            main_emotion(os.path.join(DOC_DIR,event_path))  # 情绪图
        else:
            path_list = main_weibo(event, event_id) # redis get news paths for one event
            # ./documents/topic/【怪我不够好】/【就慢一点点，孙杨不哭！】/2016-08-07 19:52
            event_path = aggregate(path_list)  # at a different time

        main_network(os.path.join(DOC_DIR,event_path))
        scale = db.get_numbers(event_id)
        db.save_refresh(event_id,scale,event_path)


if __name__ == '__main__':
    main()