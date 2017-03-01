# coding:utf-8


import urllib2
from gevent import Timeout
import requests
from bs4 import BeautifulSoup
from time import time



def probe_proxy_ip(proxy_ip):
    """代理检测"""
    proxy = urllib2.ProxyHandler(proxy_ip)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    timeout = Timeout(30)
    timeout.start()
    try:
        html = urllib2.urlopen('http://1212.ip138.com/ic.asp')
        if html:
            return True
        else:
            return False
    except Exception as e:
        print 'URLopen error'
        return False
    except Timeout:
        print 'Timeout'
        return False
    
succ = 0
fail = 0
#while True:
f = open('avalid_ip.txt', 'r')
ip_list = f.readlines()
f.close()
for ip in ip_list:
    time1 = time()
    dict = {}
    dict['http'] = ip
    if probe_proxy_ip(dict):
        succ += 1
    else:
        fail += 1
    time2 = time()
    print "succ:",succ,"failed:",fail,"time:",time2-time1,"rate:",succ*1.0/(succ+fail)

    


            
    
