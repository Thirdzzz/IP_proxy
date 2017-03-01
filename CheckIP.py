# coding:utf-8

import gevent
from gevent import monkey
monkey.patch_all()
import urllib2
from gevent.pool import Pool
from gevent import Timeout
import requests
from bs4 import BeautifulSoup
from time import time


class Checker(object):
    def __init__(self, valid_ip_file):
        self.valid_ip_file = valid_ip_file
        self.i = 0
        self.ipnum = 0
        self.check = 0
    
    def probe_proxy_ip(self, proxy_ip):
        """代理检测"""
        time1 = time()
        proxy = urllib2.ProxyHandler(proxy_ip)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        timeout = Timeout(30)
        timeout.start()
        try:
            #if (self.ipnum - self.i) < 10:
            #    return ''
            html = urllib2.urlopen('http://1212.ip138.com/ic.asp')
            time2 = time()
            self.i += 1
            print self.i, time2-time1
            # print html.read()
            if html:
                return proxy_ip['http']
            else:
                return ''
        except Exception as e:
            time2 = time()
            self.i += 1
            print self.i, time2-time1, 'URLopen error'
            return ''
        except Timeout:
            time2 = time()
            self.i += 1
            print self.i, time2-time1, 'Timeout'
            return ''


    def get_avail_ip(self, ip_file):
        ip_list = []
        with open(ip_file, 'r') as f:
            for line in f.readlines():
                dict = {}
                dict['http'] = line
                ip_list.append(dict)
                self.ipnum += 1
        print self.ipnum
        pool = Pool(100)
        succ = 0
        failed = 0
        avail_list = pool.map(self.probe_proxy_ip, ip_list)
        with open(self.valid_ip_file, 'w') as f:
            for i in range(1, len(avail_list)):
                if avail_list[i] == "" :
                    failed += 1
                else:
                    f.write(avail_list[i])
                    succ += 1
                    #print avail_list[i]
        print "succ:",succ,"failed:",failed
        if self.check < 3:
            self.check += 1
            self.get_avail_ip(self.valid_ip_file)
            
    
