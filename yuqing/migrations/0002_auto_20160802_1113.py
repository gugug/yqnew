# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yuqing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='event_id',
            field=models.IntegerField(null=True),
        ),
    ]
