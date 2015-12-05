# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from proxy.views import ProxyView, ProxyChecksView

urlpatterns = patterns('',
	url(r'check/$', ProxyChecksView.as_view(), name='proxies_checks'),
	url(r'$', ProxyView.as_view(), name='proxies_list'),

)