# coding=utf-8
__author__ = 'yc'

import MySQLdb
import datetime
import _mysql_exceptions
import json
import random
from yqnew.settings import *




class Database:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',  # 192.168.235.36 fig #192.168.1.41 me #192.168.1.40 jie
            port=3306,
            user='root',
            passwd='uliuli520',
            db='yqnew',
            charset='utf8', )

    def save_events(self,topic,keyword,info):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            ist = "insert into event(topic,check_time,keyword,information)" \
                  " values ('%s',CURRENT_DATE() ,'%s','%s')" % (topic,keyword,info)
            cur.execute(ist)
            slt = "select event_id from event order by event_id desc limit 1"
            cur.execute(slt)
            row = cur.fetchall()
            if len(row) == 0:
                # cur.execute(slt)
                # row = cur.fetchall()
                print 'bug in save events!!!!!!'
            else:
                eid = row[0]['event_id']
                cur.close()
                print '事件id',eid
                return eid

    def save_refresh(self,eid,scale,network):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "insert into eventRefresh(event_id, scale_num,refresh_time,network) " \
                  "values('%s','%s',NOW(),'%s')" % (eid,scale,network)
            cur.execute(sql)
            cur.close()
        return True

    def save_news(self, bid, eid, origin, ptime, title, content, cmt, rpt, lik):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "replace into news(blog_id, event_id,origin, post_time, title, content, comment_num, repost_num, like_num, refresh_time)" \
                  " values ('%s','%s', '%s','%s','%s','%s','%s','%s','%s',NOW())" % (
                      bid, eid, origin, ptime, title, content, cmt, rpt, lik)
            cur.execute(sql)
            cur.close()
        return True

    def update_event(self,eid,path):
        file_path = os.path.join(path,'info.txt')
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "update event set information = '%s' where event_id = '%s'" % (file_path,eid)
            cur.execute(sql)
            cur.close()

    def search_exact_topic(self,topic):
        """
        用于前端搜索框,正则匹配主题,选出对应事件的eid
        :param topic:
        :return:({event_id,etopic},{},...)
        """
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "SELECT DISTINCT event_id,topic FROM event WHERE topic ='%s'" % topic
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) == 0:
                rows = ()
                return rows
            else:
                return rows

    def search_vague_topic(self, topic):
        """
        用于前端搜索框,正则匹配主题,选出对应事件的eid
        :param topic:
        :return:({event_id,etopic},{},...)
        """
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "SELECT DISTINCT event_id,topic FROM event WHERE topic LIKE '%"+topic+"%'"
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) == 0:
                rows = ()
                return rows
            else:
                return rows

    def get_tiemline(self):
        """
        用于时间轴,提取事件与日期
        :return:({'topic': u'111', 'day': 25L, 'month': 4L},)
        """
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            # sql = "SELECT DISTINCT topic, MONTH( post_time ) AS month, DAY( post_time ) AS day "\
            #       "FROM (select * from event natural join networkscale WHERE label_dir !='None' limit 12) as temp"\
            #         " GROUP BY DATE(post_time) ORDER BY post_time ASC  LIMIT 12"
            sql = "SELECT DISTINCT topic, MONTH( check_time ) AS month, DAY( check_time ) AS day "\
                  "FROM (select * from event limit 12) as temp"\
                    " GROUP BY DATE(check_time) ORDER BY check_time ASC  LIMIT 12"
            cur.execute(sql)
            rows = cur.fetchall() #({},{}),({'topic': u'111', 'day': 25L, 'month': 4L},)
            # print 'get timeline',rows
            if len(rows) == 0:
                default = ()
                return default
            else:
                return rows

    def get_scale(self, eid):
        """
        获取事件增长规模情况图的数据
        :param eid: 事件id
        :return:
        """
        data_list = []
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select scale_num from eventRefresh where event_id = '%s' order by refresh_id desc limit 10" % eid
            cur.execute(sql)
            result = cur.fetchall()  # ({})
            if len(result) < 10:
                data_list = [11, 11, 15, 13, 12, 13, 10, 13, 12, 9]
            else:
                for i in result:
                    data_list.append(i['scale_num'])
            return data_list

    def get_network(self, eid):
        """
        获取传播路径图所需的数据
        :param eid:
        :return:
        """
        data_list = []
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select network from eventRefresh where event_id = '%s' order by refresh_id desc limit 6" % eid
            cur.execute(sql)
            result = cur.fetchall()
            if len(result) == 0:
                data_list = ['']
            else:
                for i in result:
                    data_list.append(i['network'])
        cur.close()
        return data_list

    def get_numbers(self,eid):
        """
        从news表中取出同一个事件的评论,转发,点赞,计算总规模
        :param eid: 事件id
        :return:事件规模
        """
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select sum(comment_num) as cmt, sum(repost_num) as rpt, sum(like_num) as lik from news where event_id ='%s'" % eid
            cur.execute(sql)
            result = cur.fetchall()
            if len(result[0]) == 0:
                print 'bug in getting numbers'
                return 0
            else:
                scale = result[0]['cmt'] + result[0]['rpt'] + result[0]['lik']
                return scale

    def get_news(self, eid):
        """
        获取新闻列表所需的数据并生成json文件
        :param eid: 事件id
        :return:
        """
        news_dict = {'news': []}

        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select topic,title,content,post_time,origin from news natural join event where event_id = '%s' order by blog_id desc limit 6" \
                  % eid
            cur.execute(sql)
            result = cur.fetchall()
            if len(result) == 0:
                news_dict['news'].append(
                    ({'title': 'aaaa', 'content': 'cccccc', 'post_time': '8月1日', 'origin': '人民日报'}))
                event_title = '示例事件'
            else:
                news_dict['news'] = result
                event_title = result[0]['topic']
            encode_json = json.dumps(news_dict, separators=(',', ':'))
            # print encode_json
        cur.close()
        json_file = open(os.path.join(JSON_DIR, event_title, 'news.json'), 'w+')
        json_file.writelines(encode_json)
        return True

    def get_keyword(self, eid):
        """
        获取标签云图所需的数据并生成json文件
        :param eid:
        :return:
        """
        keyword_dict = {'wordCloud': []}

        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select topic,keyword from event where event_id = '%s'" % eid
            cur.execute(sql)
            result = cur.fetchall()

            if len(result) == 0:
                result = ({'topic':'111','keyword':'aaa,bbb,ccc,ddd,'},)
                event_title = '示例事件'
            else:
                event_title = result[0]['topic']

            for i in result[0]['keyword'].split(','):
                data_dict = {}
                data_dict.setdefault('text', i)
                data_dict.setdefault('weight', str(random.randint(20, 90)))
                # print data_dict
                keyword_dict['wordCloud'].append(data_dict)
            encode_json = json.dumps(keyword_dict, separators=(',', ':'))
            print encode_json
        cur.close()
        # event_title =
        json_file = open(os.path.join(JSON_DIR, event_title, 'wordcloud.json'), 'w+')
        json_file.writelines(encode_json)
        json_file.close()
        return True


    def check_keyword(self,key_list):
        """
        检验新新闻是否已存在于数据库中
        :param key_pat:
        :return:
        """
        eid_list = []
        count_list = []
        for key_pat in key_list:
            with self.conn:
                cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
                sql = "select event_id from event where keyword regexp '%s'" % key_pat
                print sql
                cur.execute(sql)
                rows = cur.fetchall()
            if len(rows) == 0 :
                continue
            else:
                print '有重复'
                for dicts in rows:
                    id = dicts['event_id']
                    if id not in eid_list:
                        eid_list.append(id)
                        count_list.append(1)
                    else:
                        num = eid_list.index(id)
                        count_list[num] += 1
        if len(eid_list) ==0:
            return None
        else:
            m = max(count_list)
            if m >= 4:
                e_num = count_list.index(m)
                event_id = eid_list[e_num]
                print '归于事件',event_id
                return event_id
            else:
                return None
