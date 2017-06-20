#coding:utf-8
import requests
import urllib2
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import sys
import subprocess
reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderProxy(object):
    headers = {
        #"Host": "www.xicidaili.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        #"Referer": "http://www.xicidaili.com/wt/1",
    }

    def __init__(self, session_url, proxy_ip_file):
	self.session_url = session_url
	ip_list = []
	proxies = []
	with open(proxy_ip_file, 'r') as f:
		for ip in f.readlines():
			proxy = {}
			proxy['http'] = ip
			proxies.append(proxy)
	proxy = {}
	proxy['http'] = '10.10.0.236:80'
	#proxy['http'] = '10.10.0.10:80'
	proxies.append(proxy)
	self.proxies = proxies
        #self.req = requests.session()
        #self.req.get(session_url)

    def get_pagesource(self, url):
	'''
	flag = False
	for proxy in self.proxies:
		if flag:
			break
		try:
			html = requests.get(url, headers=self.headers, proxies = proxy)
			#html = requests.get(url, headers=self.headers)
			#print html.content
			flag = True
		except Exception as e:
			print "proxy ", proxy['http']," has been blocked"
	'''
        #html = self.req.get(url, headers=self.headers)
	try:
	    html = requests.get(url, headers=self.headers)
	except ConnectionError as e:
            print e
	    return ""
        return html.content

    def get_xici_proxy(self, url, n, ip_file):
        data = []
        with open(ip_file, 'a') as f:
            for i in range(1, n):
                html = self.get_pagesource(url + str(i))
		if html == "":
		    continue
                soup = BeautifulSoup(html)
		#print soup.prettify()
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

    def get_kuai_proxy(self, url, n, ip_file):
        data = []
        with open(ip_file, 'a') as f:
            for i in range(1, n):
                html = self.get_pagesource(url + str(i))
		print (url + str(i))
		if html == "":
		    continue
                soup = BeautifulSoup(html)
                for table in soup.findAll("table"):
                    for row in table.findAll("tr"):
                        cells = row.findAll("td")
                        tmp = []
                        for item in cells:
                            tmp.append(item.find(text=True))
                        if len(tmp) >= 4:
                            f.write(tmp[0] + ":" + tmp[1] + "\n")
                            data.append(tmp[0:2])
        return data

    def get_jisu_proxy(self, url, n, ip_file):
        data = []
        with open(ip_file, 'a') as f:
            html = self.get_pagesource(url)
            print url
            print html
            soup = BeautifulSoup(html)
            table = soup.find('table', id='iptable')
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                tmp = []
                for item in cells:
                    tmp.append(item.find(text=True))
                    if len(tmp) >= 3:
                        f.write(tmp[1] + ":" + tmp[2] + "\n")
                        data.append(tmp[1:3])
        return data

    def crawl(self, doc):
        try:
            cmd = './phantomjs baichuancrawler.js "%s" 90' % (doc)
            print '%s' % cmd
            stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return stdout
        except Exception as e:
            print 'Exception in crawl:%s' % e
            return ""

    def get_goubanjia_proxy(self, url, n, ip_file):
        data = []
        with open(ip_file, 'a') as f:
            for i in range(1, n):
                html = self.crawl(url + str(i) + ".shtml")
		if html == "":
		    continue
                soup = BeautifulSoup(html)
		print soup
		for table in soup.findAll("table"):
                    for row in table.findAll("tr"):
                        cells = row.findAll("td")
                        ipport = ""
                        for item in cells:
                            for s in item('p'):
                                s.extract()
                            ipport = item.text
                            f.write(ipport + "\n")
                            break
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
