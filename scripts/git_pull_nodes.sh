#!/bin/bash

for node in master node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
	ssh user@$node './git_utils.sh && exit'
done
