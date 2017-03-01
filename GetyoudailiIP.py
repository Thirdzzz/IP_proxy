#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def GetIP(ip_file):
    url = "http://www.youdaili.net/Daili/guonei/"
    headers = {
        #"Host": "www.youdaili.net",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        #"Referer": "http://www.xicidaili.com/wt/1",
    }
    
    r = requests.get(url, headers=headers);
    html = r.content
    print r.status_code
    soup = BeautifulSoup(html)
    #print soup
    pat1 = re.compile(r'href="http://www.youdaili.net/Daili/guonei/([^"]+)"')
    parts = soup.findAll('a', text=True)
    dates = []
    for item in parts:
        #print item
        #dates.append(item.find(text=True))
        if pat1.search(str(item)):
            href = (pat1.search(str(item))).group(1)
            #print href
            dates.append("http://www.youdaili.net/Daili/guonei/" + href)
    
    ip_list = []
    for url_day in dates:
        print url_day
        response = requests.get(url_day, headers=headers)
        bs = BeautifulSoup(response.content)
        p_list = bs.findAll('p', text=True)
        pat2 = re.compile(r'<p>([^"]+)@HTTP')
        for item in p_list:
            if pat2.search(str(item)):
                #print pat2.search(str(item)).group(1)
                ip_list.append(pat2.search(str(item)).group(1))
        break
            
            
    with open(ip_file, 'w') as f:
        for item in ip_list:
            f.write(item + "\n")
    

'''
with open("iplist.txt", 'w') as f:
    for i in dates:
        f.write(str(i) + "\n")
        #print str(i)
        '''
        
