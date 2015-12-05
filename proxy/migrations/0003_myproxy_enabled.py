# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0002_myproxy_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproxy',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0443\u044e\u0449\u0438\u0439 \u043b\u0438'),
        ),
    ]
