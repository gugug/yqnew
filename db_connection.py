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
            cur = self.conn(MySQLdb.cursors.DictCursor)
            ist = "insert into event(topic,occur_time,keyword,information)" \
                  " values ('%s',CURRENT_DATE() ,'%s','%s')" % (topic,keyword,info)
            cur.execute(ist)
            cur.commit()
            slt = "select event_id from event where event_id = max(event_id)"
            cur.execute(slt)
            row = cur.fetchall()
            eid = row[0]['event_id']
            cur.close()
        return eid

    def save_news(self, bid, eid, origin, ptime, title, content, cmt, rpt, lik):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "insert into news(blog_id, event_id,origin, post_time, title, content, comment_num, repost_num, like_num, refresh_time)" \
                  " values ('%s','%s', '%s','%s','%s','%s','%s','%s','%s',NOW())" % (
                      bid, eid, origin, ptime, title, content, cmt, rpt, lik)
            cur.execute(sql)
            cur.commit()
            cur.close()
        return True

    def update_event(self,eid,path):
        file_path = os.path.join(path,'info.txt')
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "update event set information = '%s' where event_id = '%s'" % (file_path,eid)
            cur.execute(sql)
            cur.commit()
            cur.close()


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
            if len(result) == 0:
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

    def get_news(self, eid):
        news_dict = {'news': []}

        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select title,content,post_time,origin from news where event_id = '%s' order by blog_id desc limit 6" \
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
            print encode_json
        cur.close()
        json_file = open(os.path.join(JSON_DIR, event_title, 'news.json'), 'w+')
        json_file.writelines(encode_json)
        return True

    def get_keyword(self, eid):
        keyword_dict = {'wordCloud': []}

        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select topic,keyword from event where event_id = '%s'" % eid
            cur.execute(sql)
            result = cur.fetchall()

            if len(result) == 0:
                result = ({'keyword': '傻逼'}, {'keyword': '二逼'}, {'keyword': '逗逼'}, {'keyword': '呆逼'})

            else:
                pass

            for i in result:
                print i.values()
                data_dict = {}
                data_dict.setdefault('text', i.values())
                data_dict.setdefault('weight', str(random.randint(20, 90)))
                print data_dict
                keyword_dict['wordCloud'].append(data_dict)
            encode_json = json.dumps(keyword_dict, separators=(',', ':'))
            print encode_json
        cur.close()
        # event_title =
        json_file = open(os.path.join(JSON_DIR, 'wordcloud.json'), 'w+')
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
            if len(rows) != 0 :
                for dicts in rows:
                    id = dicts['event_id']
                    if id not in eid_list:
                        eid_list.append(id)
                        count_list.append(1)
                    else:
                        num = eid_list.index(id)
                        count_list[num] += 1
                m = max(count_list)
                if m >= 2:
                    e_num = count_list.index(m)
                    event_id = eid_list[e_num]
                    return event_id
                else:
                    return None
            else:
                return None


# Database().get_keyword('111')
# Database().check_keyword('aaa')