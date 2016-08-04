# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.IntegerField(serialize=False, verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6id', primary_key=True)),
                ('topic', models.CharField(max_length=100, verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6\xe4\xb8\xbb\xe9\xa2\x98')),
                ('check_time', models.DateField(verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6\xe6\xa3\x80\xe6\xb5\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('keyword', models.CharField(max_length=50, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe8\xaf\x8d')),
                ('information', models.CharField(max_length=100, verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6\xe7\xbb\x9f\xe8\xae\xa1\xe4\xbf\xa1\xe6\x81\xaf\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84')),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='EventRefresh',
            fields=[
                ('refresh_id', models.IntegerField(serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.CharField(max_length=20, null=True)),
                ('refresh_time', models.DateTimeField(verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('scale_num', models.IntegerField(verbose_name=b'\xe8\xa7\x84\xe6\xa8\xa1\xe6\x80\xbb\xe9\x87\x8f')),
                ('network', models.CharField(max_length=100, verbose_name=b'\xe7\xbd\x91\xe7\xbb\x9c\xe5\x9b\xbe\xe8\xb7\xaf\xe5\xbe\x84')),
            ],
            options={
                'db_table': 'eventRefresh',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('blog_id', models.CharField(max_length=20, serialize=False, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe5\x8d\x9a\xe6\x96\x87id', primary_key=True)),
                ('event_id', models.CharField(max_length=20, null=True)),
                ('origin', models.CharField(max_length=20, verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\xba\xe6\x98\xb5\xe7\xa7\xb0')),
                ('post_time', models.DateTimeField(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4')),
                ('title', models.CharField(max_length=20, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe6\xa0\x87\xe9\xa2\x98')),
                ('content', models.TextField(max_length=500, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe5\x86\x85\xe5\xae\xb9')),
                ('comment_num', models.IntegerField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x95\xb0')),
                ('repost_num', models.IntegerField(verbose_name=b'\xe8\xbd\xac\xe5\x8f\x91\xe6\x95\xb0')),
                ('like_num', models.IntegerField(verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0')),
                ('refresh_time', models.DateTimeField(verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'news',
            },
        ),
    ]
