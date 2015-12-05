# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyProxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addr', models.CharField(max_length=16, verbose_name='IP-\u0430\u0434\u0440\u0435\u0441')),
                ('port', models.IntegerField(verbose_name='\u041f\u043e\u0440\u0442')),
                ('country', models.CharField(max_length=128, null=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True)),
                ('city', models.CharField(max_length=128, null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434', blank=True)),
                ('prtype', models.CharField(max_length=128, null=True, verbose_name='\u0422\u0438\u043f \u043f\u0440\u043e\u043a\u0441\u0438', blank=True)),
                ('anonimity', models.CharField(max_length=1, verbose_name='\u0423\u0440\u043e\u0432\u0435\u043d\u044c \u0430\u043d\u043e\u043d\u043e\u043c\u043d\u043e\u0441\u0442\u0438', choices=[(b'H', b'High'), (b'M', b'Middle'), (b'L', b'Low'), (b'N', b'None')])),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u043a\u0441\u0438-\u0441\u0435\u0440\u0432\u0435\u0440',
                'verbose_name_plural': '\u041f\u0440\u043e\u043a\u0441\u0438-\u0441\u0435\u0440\u0432\u0435\u0440\u0430',
            },
        ),
        migrations.CreateModel(
            name='ProxyCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_online', models.BooleanField(default=False, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c')),
                ('anonimity', models.BooleanField(default=False, verbose_name='\u0410\u043d\u043e\u043d\u0438\u043c\u043d\u043e\u0441\u0442\u044c')),
                ('timediff', models.FloatField(default=0.0, verbose_name='\u0422\u0430\u0439\u043c\u0430\u0443\u0442')),
                ('when_checked', models.DateTimeField(verbose_name='\u041a\u043e\u0433\u0434\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d')),
                ('proxy', models.ForeignKey(verbose_name='\u041f\u0440\u043e\u043a\u0441\u0438', to='proxy.MyProxy')),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u043e\u043a\u0441\u0438',
                'verbose_name_plural': '\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0438 \u043f\u0440\u043e\u043a\u0441\u0438',
            },
        ),
    ]
