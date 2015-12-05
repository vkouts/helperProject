from django.conf.urls import patterns, include, url
from main.views import MainView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from proxy.views import ProxyView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proxy/', include('proxy.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
