# coding=utf-8

import multiprocessing
import datetime
import redis
from combine_txt import combine_txt
from yqnew.settings import *
from crawl_headhunter import Sina
from stats_all import StatsAll
from RedisQueue import RedisQueue


__author__ = 'gu'

downredult_dir = {}

def count_time():
    """
    显示时间
    :return:
    """
    now = datetime.datetime.now()
    other_style_time = now.strftime("%Y-%m-%d %H:%M")
    print other_style_time
    return other_style_time


def get_redis_key():
    """
    链接数据库取出数据库的key, 然后生成对应的key的文件目，以便保存统计结果
    :return:
    """
    db = redis.Redis(host='192.168.235.21', port=6379, db=0)  #
    if db.dbsize():
        kes = db.keys("*")
        for i in kes:
            new_dir = os.path.join(BASE_DIR,'documents','topic1',i,count_time())
            is_exists = os.path.exists(new_dir)
            if not is_exists:
                os.makedirs(new_dir)
                # print new_dir
            downredult_dir.setdefault(i, new_dir)


def main_headunter(username):
    """
    爬用户的昵称
    :param username: 用户的昵称
    :return:
    """
    a = Sina('/n/' + str(username))
    # a.print_all()
    a.get_result()
    # a.save_txt()


def down_username(slave_num, your_id, redis_event):
    """
    下载redis的username,进行爬取资料
    username多所以用进程池来跑
    :param slave_num: 分机的数量
    :param your_id: 分机的编号，1,2,3,4....
    :return:
    """
    average = redis_event.qsize() / int(slave_num)
    slave_num = {1: [0, average], 2: [average + 1, average * 2], 3: [average * 2 + 1, average * 3],
                 4: [average * 3 + 1, average * 4], 5: [average * 4 + 1, average * 5]}

    start_num = slave_num[your_id][0]
    end_num = slave_num[your_id][1]
    username = redis_event.get_lrange(start_num, end_num)
    try:
        pool = multiprocessing.Pool(processes=8)
        print 'username>>>>>>>>>>>>>>', len(username)
        for name_index in xrange(len(username)):
            pool.apply_async(main_headunter, (username[name_index],))
        pool.close()
        pool.join()
    except Exception, e:
        print e
        pass

def do_all(func, area, age, sex):
    """
    同意调用统计地区年龄性别的方法
    :param func:统计方法
    :param area:地区
    :param age:年龄
    :param sex:性别
    :return:
    """
    func.stats_area(area)
    func.stats_age(age)
    func.stats_sex(sex)

def mul_stats(slave_num, your_id, redis_event, abs_path):
    """
    多进程统计结果
    :param slave_num: 分机的数量
    :param your_id: 分机的编号，1 2 3 4....
    :return:
    """
    try:
        down_username(slave_num, your_id,redis_event)
        all_area = Sina.area_list
        all_age = Sina.age_list
        all_sex = Sina.sex_list

        print '这么的人参与', len(all_area), ' ', len(all_age), ' ', len(all_sex)

        st = StatsAll()
        pool = multiprocessing.Pool(processes=5)
        for index in xrange(len(all_area)):
            pool.apply(do_all, (st, all_area[index], all_age[index], all_sex[index]))
        pool.close()
        pool.join()
        st.print_all()  # 打印统计结果
        st.save_all(abs_path, your_id)  # 统计结果保存在event目录下
        del Sina.area_list[:]
        del Sina.age_list[:]
        del Sina.sex_list[:]
        StatsAll.default_age_dict.clear()
        StatsAll.default_area_dict.clear()
        StatsAll.default_sex_dict.clear()

    except:
        pass


def main_down_stats(SLAVENUM, YOURID):
    """
    对数据库的多个事件处理
    :return:

    YOURID  # 机器编号
    SLAVENUM  # 机器的数量
    """

    get_redis_key()
    for topic, abs_path in downredult_dir.items():
        redis_event = RedisQueue(topic)
        # mul_stats(SLAVENUM, YOURID, redis_event, abs_path) #master选择运不运行redis
        combine_txt(abs_path, SLAVENUM)   # master等全部文件上传到后进行整合
        redis_event.del_key()   # master清空数据

# main_down_stats(1,1)

