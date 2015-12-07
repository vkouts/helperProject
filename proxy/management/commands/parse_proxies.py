# -*- coding: utf-8 -*-
__author__ = 'KucVN'
from grab import Grab
from grab.spider import Spider, Task, Data
import KVNProj.grab_settings as grab_settings
from django.core.management.base import BaseCommand
from weblib.logs import default_logging
import pytesseract
import os
import threading
from django.core.exceptions import MultipleObjectsReturned
from proxy.my_ocr import MyOCR
from proxy.models import MyProxy, ProxyCheck
import datetime
import urllib, urllib2, socket, time
import datetime
import pygeoip
import re

try:
    import Image
except ImportError:
    from PIL import Image


COUNTRIES = {
    'US': 'USA',
    'UA': 'Ukraine',
    'PL': 'Poland',
    'DE': 'Germany',
    'FR': 'France',
    'RU': 'Russia',
    'LV': 'Latvia',
    'SK': 'Slovakia',
    'BE': 'Belgium',
    'CZ': 'Czech Republic'
}

IP_CHECK_URL = 'http://ipinfo.io/ip'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
socket_timeout = 30


class HidemeProxies(Spider):
    initial_urls = ['http://hideme.ru/proxy-list/?country={country}'.format(country=x) for x in COUNTRIES.keys()]

    def task_initial(self, grab, task):
        for pr in grab.doc.select('*//table[@class="pl"]/tr[not(@class) or @class="d"]'):
            try:
                proxy_ipaddr = pr.select('./td')[0].text()
                proxy_country = pr.select('./td')[2].text()
                proxy_city = pr.select('./td')[3].text()
                proxy_type = pr.select('./td')[5].text()
                proxy_anon_ = pr.select('./td')[6].text()
                if proxy_anon_ == u'Высокая':
                    proxy_anon = 'H'
                elif proxy_anon_ == u'Средняя':
                    proxy_anon = 'M'
                else:
                    proxy_anon = 'N'
                ocr_port = 'http://hideme.ru%s' % pr.select('./td/img').attr('src')

                out_file = os.path.join(grab_settings.TMP_DIR, ocr_port.split('/')[-1])
                urllib.urlretrieve(ocr_port, out_file)
                print u'Сохранили картинку с port в %s' % out_file
                #grab.response.save(out_file)
                im = MyOCR(out_file)
                #im = MyOCR('../../.' + out_file)
                proxy_port = int(im.to_txt())
                #yield Task('ocr_image', url=ocr_port, priority=95)
                my_pr, res = MyProxy.objects.get_or_create(
                    addr=proxy_ipaddr,
                    port=proxy_port,
                    country=proxy_country,
                    city=proxy_city,
                    prtype=proxy_type,
                    anonimity=proxy_anon
                )
                if res:
                    my_pr.added = datetime.datetime.now()
                    my_pr.save()
            except Exception, err:
                print Exception, err


def hideme_parse():
    default_logging(grab_log=grab_settings.GRAB_LOG, network_log=grab_settings.NETWORK_LOG)
    bot = HidemeProxies(thread_number=1)
    bot.run()


class FoxToolsProxy(Spider):
    initial_urls = ['http://foxtools.ru/Proxy?country={country}'.format(country=x) for x in COUNTRIES.keys()]

    def task_initial(self, grab, task):
        for pr in grab.doc.select('*//table[@id="theProxyList"]/tbody/tr'):
            proxy_ipaddr = pr.select('./td')[1].text()
            proxy_port = pr.select('./td')[2].text()
            proxy_country = pr.select('./td')[3].text()
            proxy_anon_ = pr.select('./td')[4].text()
            proxy_type = pr.select('./td')[5].text()

            for im in COUNTRIES.keys():
                if '(%s)' % im in proxy_country:
                    proxy_country = COUNTRIES[im]

            if proxy_anon_ == u'наивысшая':
                proxy_anon = 'H'
            elif proxy_anon_ == u'высокая':
                proxy_anon = 'M'
            else:
                proxy_anon = 'N'
            my_pr, res = MyProxy.objects.get_or_create(
                addr=proxy_ipaddr,
                port=proxy_port,
                country=proxy_country,
                city=u'',
                prtype=proxy_type,
                anonimity=proxy_anon
            )
            if res:
                my_pr.added = datetime.datetime.now()
                my_pr.save()


def foxtools_parse():
    default_logging(grab_log=grab_settings.GRAB_LOG, network_log=grab_settings.NETWORK_LOG)
    bot = FoxToolsProxy(thread_number=1)
    bot.run()


socket.setdefaulttimeout(socket_timeout)

# Get real public IP address
def get_real_pip():
    req = urllib2.Request(IP_CHECK_URL)
    req.add_header('User-agent', user_agent)
    conn = urllib2.urlopen(req)
    page = conn.read()
    return page.strip()


def check_proxy(prox, my_real_ip):
    proxy_checks = ProxyCheck.objects.filter(proxy=prox)
    if not my_real_ip:
        my_real_ip = get_real_pip()
    ipaddr = '%s:%s' % (prox.addr, prox.port)
    try:
        proxy_handler = urllib2.ProxyHandler({'http': ipaddr})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        #req=urllib2.Request('http://www.google.com')
        req = urllib2.Request(IP_CHECK_URL)  # change the url address here
        time_start = time.time()
        sock = urllib2.urlopen(req)
        time_end = time.time()
        detected_ip = sock.read().strip()
        anonimity = False if detected_ip == my_real_ip else True
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code

        res, anon, timediff = False, False, 0
    except Exception, detail:
        print "ERROR:", detail
        res, anon, timediff = False, False, 0
    res, anon, timediff = True, anonimity, time_end - time_start
    if res:
        my_chk = ProxyCheck.objects.create(
            proxy=prox,
            is_online=True,
            anonimity=anon,
            timediff=timediff,
            when_checked=datetime.datetime.now()
        )
        my_chk.save()
        prox.checked = True
        prox.save()
        print u'%s:%s рабочий' % (prox.addr, prox.port)
    else:
        my_chk = ProxyCheck.objects.create(
            proxy=prox,
            is_online=False,
            anonimity=False,
            timediff=0.0,
            when_checked=datetime.datetime.now()
        )
        my_chk.save()
        prox.checked = True
        prox.save()
        print u'%s:%s нерабочий' % (prox.addr, prox.port)

    if proxy_checks.count() == proxy_checks.filter(is_online=False) and proxy_checks.count() >= 2:
        prox.enabled = False
        prox.save()


def check_my_proxyes():
    my_real_ip = get_real_pip()
    for im in MyProxy.objects.filter(enabled=True):
        t = threading.Thread(check_proxy, args=(im, my_real_ip))
        t.start()




def textproxy_parse(myfile):
    my_real_ip = get_real_pip()

    ipaddr_re = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+).*')
    gi = pygeoip.GeoIP(os.path.join('.', 'proxy', 'import', 'GeoIP.dat'))
    with open(myfile, 'r') as proxies:
        for im in proxies:
            addr_ = ipaddr_re.match(im)
            if addr_:
                addr = addr_.group(1)
                port = addr_.group(2)

                res, anon, timediff = check_proxy(addr, port, my_real_ip)

                if res:
                    try:
                        my_prx, res1 = MyProxy.objects.get_or_create(
                            addr=addr,
                            port=port,
                            country=gi.country_name_by_addr(addr),

                        )
                        if res1:
                            my_prx.save()
                    except MultipleObjectsReturned:
                        # если получаем более чем один объект - берем только первый
                        my_prx = MyProxy.objects.filter(
                            addr=addr,
                            port=port,
                            country=gi.country_name_by_addr(addr),
                        ).first()

                    my_chk = ProxyCheck(
                        proxy=my_prx,
                        check=True,
                        anonimity=anon,
                        timediff=timediff,
                        when_checked=datetime.datetime.now()
                    )
                    my_chk.save()
                    my_prx.checked = True
                    my_prx.save()
                    print 'Added', addr, port, gi.country_name_by_addr(addr)
                else:
                    print addr, 'Not worked'


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получаем сначала свой реальный ip
        my_real_ip = get_real_pip()
        print my_real_ip
        #hideme_parse()
        foxtools_parse()
        check_my_proxyes()

    #textproxy_parse(os.path.join('.', 'proxy', 'import', 'proxylist_at_10.07.2015.txt'))
    #print os.listdir(os.path.join('.', 'proxy', 'import'))


