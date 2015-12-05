# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, FormView, TemplateView
from django.shortcuts import render
from proxy.models import MyProxy, ProxyCheck
from django.conf import settings

# Create your views here.
class ProxyView(ListView):
	template_name = 'proxy_view.html'
	model = MyProxy
	paginate_by = 20

	def get_queryset(self):
		return self.model.objects.all().order_by('-added')


class ProxyChecksView(ListView):
	template_name = 'proxy_check_view.html'
	model = ProxyCheck
	paginate_by = 20

	def get_queryset(self):
		return self.model.objects.all().order_by('-when_checked')
