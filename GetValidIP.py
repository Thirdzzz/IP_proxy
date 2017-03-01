# coding:utf-8

from GetxiciIP import SpiderProxy
import GetyoudailiIP
from CheckIP import Checker
from time import time


if __name__ == '__main__':
    ip_file = 'iplist.txt'
    valid_ip_file = 'avalid_ip.txt'

    #youdaili
    GetyoudailiIP.GetIP(ip_file)

    #xicidaili
    session_url = 'http://www.xicidaili.com/wt/1'
    url = 'http://www.xicidaili.com/wt/'
    p = SpiderProxy(session_url)
    proxy_ip = p.get_all_proxy(url, 5, ip_file)

    #check ip available
    time1 = time()
    checker = Checker(valid_ip_file)
    checker.get_avail_ip(ip_file)
    time2 = time()
    print time2 - time1


