#!/bin/bash

curl http://www.66ip.cn/mo.php?tqsl=2000 > 66ip.html
cat 66ip.html | grep "<br" | awk '{print $1}' | awk -F"<" '{print $1}' | sort | uniq > 66ip.txt
