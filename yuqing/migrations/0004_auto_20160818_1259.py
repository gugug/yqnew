# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yuqing', '0003_auto_20160802_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='topic',
            field=models.CharField(max_length=200, verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6\xe4\xb8\xbb\xe9\xa2\x98'),
        ),
    ]
