# coding:utf-8 
from CheckIP import Checker
from time import time

if __name__ == '__main__':
	ip_file = 'uniq_ip.txt'
	valid_ip_file = 'avalid_ip.txt'

	time1 = time()
	checker = Checker(valid_ip_file)
	checker.get_avail_ip(ip_file)
	time2 = time()
	print time2 - time1
