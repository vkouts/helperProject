# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproxy',
            name='added',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d', blank=True),
        ),
    ]
