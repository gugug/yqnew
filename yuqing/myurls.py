#coding=utf-8
from django.conf.urls import url
from yuqing.views import *

__author__ = 'yc'

urlpatterns=[
    # url(r'^network/(?P<event_id>[^/]+)/(?P<ctime>[^/]+)/$',network,name='network'),
    # url(r'^linechart/(?P<topic>[^/]+)/$',line_chart,name='linechart'),
    url(r'graphs/$',graph,name='graph'),
    url(r'test/$',test,name='test'),
    url(r'repost/$',repost,name='repost')

]
