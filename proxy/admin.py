#-*- coding: utf-8 -*-
from django.contrib import admin
from proxy.models import MyProxy, ProxyCheck

# Register your models here.
class MyProxyAdmin(admin.ModelAdmin):
	list_display = ('addr', 'port', 'country', 'city', 'prtype', 'anonimity')

class MyProxyCheckAdmin(admin.ModelAdmin):
	list_display = ('when_checked', 'proxy', 'is_online', 'anonimity', 'timediff')

	def get_countr(self,obj):
		return obj.proxy.country

	get_countr.short_description = u'Страна'
	get_countr.admin_order_field = 'proxy__country'

admin.site.register(MyProxy, MyProxyAdmin)
admin.site.register(ProxyCheck, MyProxyCheckAdmin)
