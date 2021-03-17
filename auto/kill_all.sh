#!/bin/bash

for node in master node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
	if [ $node = "master" ]; then
		sshpass -p vmm ssh user@83.212.74.75 "~/Distributed-NTUA/auto/kill_me.sh && exit"
	else
		sshpass -p vmm ssh user@83.212.74.75 "ssh user@$node "~/Distributed-NTUA/auto/kill_me.sh && exit""

	fi

done

# ps aux |grep python |awk '{print $2}' |xargs kill
# ps aux |grep python |grep -v 'pattern_of_process_you_dont_want_to_kill' |awk '{print $2}' |xargs kill
