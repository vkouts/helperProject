# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0003_myproxy_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myproxy',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 19, 58, 35, 581000, tzinfo=utc), verbose_name='\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d', auto_now_add=True),
            preserve_default=False,
        ),
    ]
