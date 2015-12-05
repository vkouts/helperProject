# -*- coding: utf-8 -*-
from django.db import models


class MyProxy(models.Model):
    ANON_CHOICES = (
    ('H', 'High'),
    ('M', 'Middle'),
    ('L', 'Low'),
    ('N', 'None'),
    )
    addr = models.CharField(verbose_name=u'IP-адрес', max_length=16)
    port = models.IntegerField(verbose_name=u'Порт')
    country = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'Страна')
    city = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'Город')
    prtype = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'Тип прокси')
    anonimity = models.CharField(max_length=1, choices=ANON_CHOICES, verbose_name=u'Уровень анономности')
    added = models.DateTimeField(auto_now_add=True, verbose_name=u'Добавлен')
    enabled = models.BooleanField(default=True, verbose_name=u'Действующий ли')


    def __unicode__(self):
        return "%s:%s" % (self.addr, str(self.port))

    class Meta:
        verbose_name = u'Прокси-сервер'
        verbose_name_plural = u'Прокси-сервера'


class ProxyCheck(models.Model):
    proxy = models.ForeignKey(MyProxy, verbose_name=u'Прокси')
    is_online = models.BooleanField(default=False, verbose_name=u'Доступность')
    anonimity = models.BooleanField(default=False, verbose_name=u'Анонимность')
    timediff = models.FloatField(default=0.0, verbose_name=u'Таймаут')
    when_checked = models.DateTimeField(verbose_name=u'Когда проверен')

    class Meta:
        verbose_name = u'Проверка прокси'
        verbose_name_plural = u'Проверки прокси'