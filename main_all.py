# coding=utf-8
__author__ = 'yc'

# import redis
# import redis.exceptions
import time
import multiprocessing as mul
import shutil
from EventAnalysis.BlogSearch.main_crawler import *
from EventDectection.EventDection import *
from KeyExtract.key_extract import *
from EventAnalysis.links_labels import *
from db_connection import *
from EventAnalysis.RedisDj import *
from Emotion.e1 import *
# from EventAnalysis.info.attempt_three import *
from EventAnalysis.RedisDj.Crawler.main_hunter import *
from django.db import connection


def aggregate(path_list):
    """
    把属于同一个事件的新闻数据聚合起来
    :param path_list: 同事件的新闻文件夹路径
    :return:
    """
    split_path = path_list[0].split('/')
    event = split_path[3]
    time = split_path[5]
    all_path = os.path.join(event, time)
    folder_path = os.path.join(DOC_DIR, all_path)
    print "aggregating folder path:", folder_path
    if os.path.exists(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    all_cmt = open(os.path.join(DOC_DIR, all_path, 'comment.txt'), 'a+')
    all_par = open(os.path.join(DOC_DIR, all_path, 'participants.txt'), 'a+')
    all_rpt = open(os.path.join(DOC_DIR, all_path, 'repost_path.txt'), 'a+')
    for path in path_list:
        cmt_file = open(os.path.join(path, 'comment.txt'), 'r')
        all_cmt.writelines(cmt_file.readlines())
        cmt_file.close()

        par_file = open(os.path.join(path, 'participants.txt'), 'r')
        all_par.writelines(par_file.readlines())
        par_file.close()

        rpt_file = open(os.path.join(path, 'repost_path.txt'), 'r')
        all_rpt.writelines(rpt_file.readlines())
        rpt_file.close()

    all_rpt.close()
    all_par.close()
    all_cmt.close()
    return all_path


def copy_file(topic_list):
    """
    copy the local json file to the server
    :param topic_list:
    :return:
    """
    print 'len topic list', len(topic_list)
    upload_dir = '/home/monkeys/yqnew/upload/data'
    os.makedirs(upload_dir)
    for topic in topic_list:
        upload_path = os.path.join(upload_dir, topic)
        if not os.path.isdir(upload_path):
            print "准备创建文件夹"
            os.makedirs(upload_path)
        else:
            print 'folder exists'
        file_path = os.path.join(JSON_DIR, topic)
        for paths, folders, files in os.walk(file_path):
            for i in files:
                upload_file = os.path.join(upload_path, i)
                if not os.path.isfile(upload_file):
                    print '准备上传事件', topic, '的文件', upload_file
                    shutil.copy2(os.path.join(JSON_DIR, topic, i), upload_file)
                else:
                    print '本事件已在上传列表中'

    os.system('scp -r /home/monkeys/yqnew/upload/data root@42.96.134.205:/root/yqnew/static/')
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)

    print '上传完成'


def check_event(num, checked_event_list, event):
    undected_list = []
    for news in event:
        state = False
        for old_news in checked_event_list[num][0]:
            if news == old_news:
                state = True
        if not state:
            undected_list.append(news)
    return undected_list


def sleep(flag=0):
    """
    control the sleeping time
    :param flag: flag =0 : normal run, sleep 7200s; flag = 1: recovery, sleep 1200s; flag = 2, test, sleep 600s
    :return:
    """
    if flag == 0:
        time.sleep(600)
    elif flag == 1:
        time.sleep(300)
    else:
        time.sleep(300)
    return True


def main():
    checked_event_list = []
    topic_list = []

    # [[list]]
    user = MoblieWeibo()
    # user.login('meiou074434144@163.com', 'aaa333')
    # user.login('meishikuidao3@163.com', 'aaa333')
    # user.login('men27526@163.com', 'aaa333')
    user.login('70705420yc@sina.com', '1234567')
    # user.login('451650276@qq.com', '19950602')
    # user.login('18826103516', '19950602')

    flag = 0
    sums = 0
    while True:
        sleep_flag = 0
        db = Database()
        # print '已检测事件:'
        for i in topic_list:
            print i
        print '正在追踪已检测过的事件'

        for package in checked_event_list:  # package: ([event],event_id,keywords)
            for i in package[0]:
                print 'event!!!!!!!!!!!!!!', i

            topic = db.get_event(package[1])
            path_list = main_weibo(package[0], package[1])  # follow
            news_tuple = start_search(package[2], topic[0]['topic'], 1)  # use keywords to search new news
            if news_tuple is not None:
                if not news_tuple[4] == '未知':
                    db.save_news(news_tuple[0], package[1], news_tuple[2], news_tuple[3], news_tuple[4], news_tuple[1],
                                 news_tuple[7], news_tuple[6], news_tuple[5])
                    path_list.append(news_tuple[8])
            print 'pl', path_list
            if len(path_list) != 0:
                event_path = aggregate(path_list)
                main_network(os.path.join(DOC_DIR, event_path))
                scale = db.get_numbers(package[1])
                db.save_refresh(package[1], scale, event_path)
            else:
                print "请殴打才良"

        # time.sleep(random.randint(30, 60))
        events = []
        if sums == 0:
            print '正在检测新事件'
            events = detect_event()
            # events = [
            #    ['【乔任梁去世追思会9月22日上午9时上海举行】', '送别乔任梁'],['陈乔恩哭了'],['乔任梁死亡','【网曝乔任梁上海死亡 身上有伤疑为自残】',
            #     '【乔任梁死亡轰动娱乐圈 群星发文哀悼[蜡烛]】'], ['送别乔任梁 乔任梁曾在朋友圈写下前提是问心无愧', '追思会现场曝光 粉色鲜花布置',
            #     '今夜无眠，你带着我初中时代的追星回忆一起离开了'],
            #    ['【老布什表示将投票给希拉里】','为问鼎白宫 希拉里特朗普这两位老人到底有多拼','','特朗普对希拉里[微笑]','希拉里健康问题',
            #     '美国 民主党 总统 候选人 希拉里 取消 西海岸 行程','希拉里今年6月受访时抽搐视频曝光','希拉里911纪念会后昏倒','真假希拉里'
            #     ]
            # ]
            print "events_events", len(events)
            sums = 7
        db = Database()  # 激活数据库
        for event in events:
            print "event>>>>>", event
            time.sleep(random.randint(5, 10))
            s = ''
            keyword_list = main_keyword(event)
            for i in keyword_list:
                s += i
                s += ','
            event_id = db.check_keyword(keyword_list)
            if event.__len__() == 0:
                continue
            # 新事件
            if event_id is None:
                db = Database()  # 激活数据库
                event_id = db.save_events(event[0], s, 'null')
                print '新事件,id', event_id
                path_list = main_weibo(event, event_id)  # redis get news paths for one event
                # ./documents/topic/【怪我不够好】/【就慢一点点，孙杨不哭！】/2016-08-07 19:52
                if len(path_list) != 0:
                    event_path = aggregate(path_list)
                    db = Database()  # 激活数据库
                    db.update_event(event_id, event_path)
                    # main_info(os.path.join(DOC_DIR,event_path))  # 年龄,地图
                    main_emotion(os.path.join(DOC_DIR, event_path))  # 情绪图

                    main_network(os.path.join(DOC_DIR, event_path))
                    db = Database()  # 激活数据库
                    scale = db.get_numbers(event_id)
                    db.save_refresh(event_id, scale, event_path)
                    news_list = db.get_news_list(event_id)
                    checked_event_list.append((news_list, event_id, s.replace(',', ' ')))  # [(event_id, keywords)]
                    topic_list.append(event[0])
                else:
                    print "见到才良，直接打死，算我的"

            # 与旧事件重复,已有event_id
            else:
                print "正在检测旧事件列表"
                num = -1
                for i in range(len(checked_event_list)):
                    if event_id == checked_event_list[i][1]:
                        num = i
                        break
                print num
                if num == -1:  # 前一次因bug断开,checked list中不存在结果而数据库中有数据保留
                    print '正在从上一次断开中恢复'
                    db = Database()  # 激活数据库
                    news_list = db.get_news_list(event_id)
                    checked_event_list.append((news_list, event_id, s.replace(',', ' ')))
                    topic_list.append(event[0])
                    sleep_flag = 1

                else:
                    undected_list = check_event(num, checked_event_list, event)
                    print '归于旧事件', checked_event_list[num][1]
                    for i in undected_list:
                        checked_event_list[num][0].append(i)

        main_hunter()  # 年龄,地图
        if re.findall('0[0-6]:', str(datetime.datetime.now())) is not None:
            checked_event_lsit = []
        print '正在统一数据库与文件夹'
        db = Database()  # 激活数据库
        db.unification()
        print '正在复制文件到服务器'
        copy_file(topic_list)

        print '完成1次检测,下一次检测将稍后开始'
        sleep(sleep_flag)
        sums -= 1


if __name__ == '__main__':
    main()
