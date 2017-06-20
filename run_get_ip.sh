#!/bin/bash 
python GetValidIP.py

curl http://www.66ip.cn/mo.php?tqsl=2000 > 66ip_html_new
content=`cat 66ip_html_new`
if [[ "$content" != "" ]];then
	cp 66ip_html_new 66ip.html
fi
cat 66ip.html | grep "<br" | awk '{print $1}' | awk -F"<" '{print $1}' >> tmp_ip.txt
cat 66ip.txt | grep "<br" | awk '{print $1}' | awk -F"<" '{print $1}' >> tmp_ip.txt

cat tmp_ip.txt | sort | uniq > uniq_ip.txt
echo `date`
