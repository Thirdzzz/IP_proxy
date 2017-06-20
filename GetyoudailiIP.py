#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import sys
import urllib2
from requests.exceptions import ConnectionError
reload(sys)
sys.setdefaultencoding( "utf-8" )

def Download(host, ip_list, thousand):
    url = host
    headers = {
        #"Host": "www.youdaili.net",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        #"Referer": "http://www.xicidaili.com/wt/1",
    }
    try:
        r = requests.get(url, headers=headers);
    except ConnectionError as e:
        print e
        return []
    html = r.content
    print r.status_code
    soup = BeautifulSoup(html)
    #print soup
    pat1 = re.compile('href="' + host + '([^"]+)"')
    parts = soup.findAll('a', text=True)
    dates = []
    for item in parts:
        if pat1.search(str(item)):
            href = (pat1.search(str(item))).group(1)
            dots = href.split('.')
            dates.append(host + href)
            dates.append(host + dots[0] + "_2.html")
            dates.append(host + dots[0] + "_3.html")
            dates.append(host + dots[0] + "_4.html")
            dates.append(host + dots[0] + "_5.html")
    
    num = 0
    for url_day in dates:
        num += 1
        print url_day
        try:
	    response = requests.get(url_day, headers=headers)
	except ConnectionError as e:
            print e
            continue
        bs = BeautifulSoup(response.content)
        p_list = bs.findAll('p', text=True)
        pat2 = re.compile(r'<p>([^"]+)@HTTP')
        for item in p_list:
            if pat2.search(str(item)):
                #print pat2.search(str(item)).group(1)
                ip_list.append(pat2.search(str(item)).group(1))
        if num > thousand * 10:
            return ip_list

def GetIP(ip_file):
    ip_list = []
    ip_list = Download('http://www.youdaili.net/Daili/guonei/', ip_list, 4)
    ip_list = Download('http://www.youdaili.net/Daili/QQ/', ip_list, 4)
    ip_list = Download('http://www.youdaili.net/Daili/http/', ip_list, 4)
            
    with open(ip_file, 'w') as f:
        for item in ip_list:
            f.write(item + "\n")
    

'''
with open("iplist.txt", 'w') as f:
    for i in dates:
        f.write(str(i) + "\n")
        #print str(i)
        '''
        
