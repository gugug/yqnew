# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yuqing', '0002_auto_20160802_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrefresh',
            name='event_id',
            field=models.IntegerField(null=True),
        ),
    ]
