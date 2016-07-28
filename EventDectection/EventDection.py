#coding=utf-8
from NewsDection import NewsDetection
from cluster import Cluster


def detect_event():
    news_detection = NewsDetection()
    dict_news = news_detection.get_dic_news()
    cluster = Cluster(dict_news)
    news_clusters = cluster.cluster_news()
    for one_cluster in news_clusters:
        if one_cluster.__len__() < 3:
            news_clusters.remove(one_cluster)
            continue
        print '--------'
        for news in one_cluster:
            print news
    events = news_clusters
    return events

if __name__ == '__main__':
    events = detect_event()
    print '*****'
    for i in events:
        print events