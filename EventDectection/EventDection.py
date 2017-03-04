# coding=utf-8
import random
import urllib2

from NewsDection import NewsDetection, MoblieWeibo
from cluster import Cluster
import sys
import re

sys.path.append('../EventAnalysis/BlogSearch/')


def detect_event():  # main
    news_detection = NewsDetection()
    dict_news = news_detection.get_dic_news()
    cluster = Cluster(dict_news)
    news_clusters = cluster.cluster_news()
    result_clusters = list()
    for one_cluster in news_clusters:
        if one_cluster.__len__() < 3:
            continue
        print '--------'

        for news in one_cluster:
            print news
        result_clusters.append(one_cluster)
    events = result_clusters

    new_events = []
    for event in events:
        x_news = []
        for news in event:
            if news_is_valid(news):  #去除不对应的新闻
                x_news.append(news)
        new_events.append(x_news)

    return new_events


def get_topic(topic_words,content):
        """
        :param content:博文内容
        :return:博文主题
        """
        topic_patternts = re.compile(topic_words+'</span>')
        topic = topic_patternts.findall(content)
        if len(topic) > 0:
            print topic_words, '成功对应'
            return True
        else:
            print topic_words, "这篇博文对应话题，检测不到"
            return False


def news_is_valid(topic_words):
    topic_words = str(topic_words)
    page = 1
    pageurl = 'http://weibo.cn/search/mblog?keyword=' + str(
                    urllib2.quote(topic_words)) + '&sort=hot&page=' + str(page)
    header = {'User-Agent': 'Mozilla/' + str(
            float(int(random.uniform(1, 6)))) + '(X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/' + str(
            float(int(random.uniform(29, 36))))}
    req = urllib2.Request(url=pageurl, headers=header)
    content = urllib2.urlopen(req).read()
    flag = get_topic(topic_words, content)
    return flag

#
# if __name__ == '__main__':
#     user = MoblieWeibo()
#     user.login('70705420yc@sina.com', '1234567')
#     events = detect_event()
#     print '*****'
#     new_events=[]
#     for event in events:
#         X_news = []
#         for news in event:
#             if news_is_valid(news):
#                 X_news.append(news)
#         new_events.append(X_news)
#
#     for i in new_events:
#         for j in i:
#             print j
#         print '------'
#

