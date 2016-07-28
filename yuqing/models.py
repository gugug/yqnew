# coding=utf-8
from django.db import models
from django.contrib import admin

# Create your models here.

class Event(models.Model):
    event_id = models.CharField('事件id', max_length=20, primary_key=True)
    topic = models.CharField('事件主题', max_length=100)
    occur_time = models.DateField('事件检测时间')
    keyword = models.CharField('关键词', max_length=50)
    information = models.CharField('事件统计信息文件路径', max_length=100)

    def __unicode__(self):
        return u'%s %s' % (self.event_id, self.topic)

    class Meta:
        db_table = 'event'


class News(models.Model):
    blog_id = models.CharField('新闻博文id', max_length=20, primary_key=True)
    event_id = models.ForeignKey(Event, related_name='event_id', to_field='event_id')
    origin = models.CharField('发起人昵称', max_length=20)
    post_time = models.DateTimeField('新闻发布时间')
    title = models.CharField('新闻标题', max_length=20)
    content = models.TextField('新闻内容', max_length=500)
    comment_num = models.IntegerField('评论数')
    repost_num = models.IntegerField('转发数')
    like_num = models.IntegerField('点赞数')
    refresh_time = models.DateTimeField('更新时间')

    def __unicode__(self):
        return u'%s %s' % (self.blog_id, self.title)

    class Meta:
        db_table = 'event'


class EventRefresh(models.Model):
    refresh_id = models.IntegerField(auto_created=True, primary_key=True)
    event_id = models.ForeignKey(Event, related_name='event_id', to_field='event_id')
    refresh_time = models.DateTimeField('更新时间')
    scale_num = models.IntegerField('规模总量')
    network = models.CharField('网络图路径', max_length=100)

    def __unicode__(self):
        return u'%s %s' % (self.event_id, self.check_time)

    class Meta:
        db_table = 'eventRefresh'
