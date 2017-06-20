#!/bin/bash 
dir=`pwd`
if [ ! -f uniq_ip.txt ];then
	touch uniq_ip.txt
fi
while [ 1 ]
do
	python $dir/checker.py
	cat avalid_ip.txt | sort | uniq > avalid_ip_uniq.txt
	shuf avalid_ip_uniq.txt -o ../outer_iplist.txt
	echo `date`
	sleep 5
done
