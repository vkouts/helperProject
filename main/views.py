# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View, TemplateView
from django.shortcuts import render

# Create your views here.
class MainView(TemplateView):
    template_name = "main_view.html"
