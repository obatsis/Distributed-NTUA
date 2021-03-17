#!/bin/bash

for node in master node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
	if [ $node = "master" ]; then
		sshpass -p vmm ssh user@83.212.74.75 "ps aux |grep python |awk '{print $2}' |xargs kill && exit"
	else
		sshpass -p vmm ssh user@83.212.74.75 "ssh user@$node 'ps aux |grep python |awk '{print $2}' |xargs kill && exit'"

	fi

done
