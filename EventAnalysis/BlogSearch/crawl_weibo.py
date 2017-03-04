# coding=utf-8

import random
import sys
from time import sleep
import urllib2
import re
from create_file import *
from multiprocessing import Process, Manager
import os
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'gu'
"""
7.27
测试完毕
"""


class WeiboPage:
    """
    父类
    定义了一些变量和一些公用方法
    """
    manager = Manager()
    detected_tpdict = {}
    detected_tpdict = manager.dict()
    all_hunterlist = []
    all_hunterlist = manager.list()  # 保存猎头的全部博文,点赞之类的

    def __init__(self):
        """
        :param one_user: 用户的id，即是猎头的id
        :return:
        """
        self.weibo_list = []
        self.time_list = []
        self.weibo = []
        self.writing_time = []
        self.base_page = []
        self.dictwt = {}
        self.no_repeat_list = []
        self.comment_dir = os.path.join(BASE_DIR, 'documents', 'comment/')  # 猎头微博的评论内容
        self.forward_path_dir = os.path.join(BASE_DIR, 'documents', 'forward_path/')  # 猎头的微博的转发路径
        self.header = {'User-Agent': 'Mozilla/' + str(
            float(int(random.uniform(1, 6)))) + '(X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/' + str(
            float(int(random.uniform(29, 36))))}

        self.blog_id = ''
        self.post_time = ''
        self.event_id = ''
        self.corpus_dir = ''
        self.link = ''

    def cleaned_wbtime(self, item1):
        """
        转化时间格式
        :param item1: 时间
        :return:标准格式的时间 h:m:s
        """
        extra = re.compile('</span>.*$')  # 匹配输入字符串的结束位置
        today = re.compile('今天')
        ago = re.compile('\d+分钟前')

        post_time = re.sub(extra, '', item1)
        t = time.strftime('%m' + '月' + '%d' + '日', time.localtime())
        t = t.decode('utf-8')
        post_time = re.sub(today, t, post_time)
        post_time = re.sub(ago, t, post_time)
        return post_time

    def cleaned_weibo(self, item0):
        """
        净化博文
        :param item0:博文
        :return:净化干净的博文
        """
        sub_title = re.compile('<img.*?注')
        tag = re.compile('<.*?>')  # 去除标签
        link = re.compile('<a href=.*?>|http.*?</a>')  # 去除链接
        content = re.sub(link, "", item0)
        content = re.sub(tag, '', content)
        content = re.sub(sub_title, '', content)
        return content

    def get_forward_common(self, forward_url):
        """
        匹配转发路径及理由，用列表返回
        :param forward_url: 转发页的链接
        :return:该页的转发路径及理由

        # forward1_patterns = re.compile(
        #     '//<a href="/n.*?>(@.*?)</a>:(.*?)&nbsp;')  # 去除最后一个转发者的路径
        # forward_participants_pattern = re.compile(
        #     '<div class="c"><a href="/\D.*?">(.*?)</a>'
        # )
        # forward_participants = forward_participants_pattern.findall(forward_page)
        """
        time.sleep(random.randint(1, 4))
        req = urllib2.Request(url=forward_url, headers=self.header)
        forward_page = urllib2.urlopen(req).read()
        time.sleep(int(random.uniform(0, 2)))

        forward_participants = []
        forward_string_list = []

        total_pattern = re.compile('</form></div>(<div class="c">.*?)<form action')  # 匹配一大块
        text = re.findall(total_pattern, forward_page)

        forward_patterns = re.compile('<div class="c">.*?<a href=".*?>(.*?)</a>(.*?)<span class="cc">')
        label_pattern = re.compile('<.*?>')
        space_pattern = re.compile('&nbsp;')

        if not len(text):
            # print forward_url
            pass
        else:
            forward_path = forward_patterns.findall(text[0])
            for k in forward_path[0:]:
                k1 = re.sub(label_pattern, '', k[1])
                k1 = re.sub(space_pattern, '', k1)
                k1 = re.sub('http.*?$', '', k1)
                forward_string = str(k[0]) + str(k1)
                forward_string_list.append(forward_string)
                forward_participants.append(k[0])

        forward_list = list(set(forward_string_list))
        forward_list.sort(key=forward_string_list.index)
        return forward_list, forward_participants  # 返回转发路径和博文源,参与人

    def get_comment_common(self, cmt_url):
        """
        :param cmt_url: 评论的页数
        :return: comment_list, comment_participants 该页的评论内容和参与人
        """
        comment_list = []
        comment_participants = []
        time.sleep(random.randint(1, 4))
        req = urllib2.Request(url=cmt_url, headers=self.header)
        comment_page = urllib2.urlopen(req).read()
        time.sleep(int(random.uniform(0, 2)))

        comment_patterns = re.compile(
            '>        <a href="/.*?">(.*?)</a>    .*?    :<span class="ctt">(.*?)</span>    &nbsp;'
        )
        label_pattern = re.compile('<.*?>')
        comment = comment_patterns.findall(comment_page)
        for i in comment:
            name = re.sub(label_pattern, '', i[0])
            comm1 = re.sub(label_pattern, '', i[1])
            comm2 = re.sub('http.*?$', '', comm1)  # 去除链接
            comm3 = re.sub('//', '', comm2)
            comm = re.sub('&nbsp;(.*?)来自', '', comm3)
            com = str(name) + ' : ' + str(comm)
            comment_list.append(com)
            comment_participants.append(name)

        return comment_list, comment_participants
