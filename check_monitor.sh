#!/bin/bash
dir=`pwd`
pid=`ps -ef | grep $dir/run_check.sh | egrep -v 'grep' | awk '{print $2}'`
if [ "$pid" == "" ];then
	nohup $dir/run_check.sh &
fi
