#coding:utf-8
import requests
from bs4 import BeautifulSoup


class SpiderProxy(object):
    headers = {
        #"Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        #"Referer": "http://www.xicidaili.com/wt/1",
    }

    def __init__(self, session_url):
        self.req = requests.session()
        self.req.get(session_url)

    def get_pagesource(self, url):
        html = self.req.get(url, headers=self.headers)
        return html.content

    def get_all_proxy(self, url, n, ip_file):
        data = []
        with open(ip_file, 'a') as f:
            for i in range(1, n):
                html = self.get_pagesource(url + str(i))
                soup = BeautifulSoup(html)
                #soup = soup.prettify()
                table = soup.find('table', id="ip_list")
                for row in table.findAll("tr"):
                    cells = row.findAll("td")
                    tmp = []
                    for item in cells:
                        tmp.append(item.find(text=True))
                    if len(tmp) >= 2:
                        f.write(tmp[1] + ":" + tmp[2] + "\n")
                    #print tmp
                    data.append(tmp[1:3])
        return data

'''

session_url = 'http://www.xicidaili.com/wt/1'
url = 'http://www.xicidaili.com/wt/'
p = SpiderProxy(session_url)
proxy_ip = p.get_all_proxy(url, 2, ip_file)
n = 0
for item in proxy_ip:
    n += 1    
    if item:
        print item
print n
'''
