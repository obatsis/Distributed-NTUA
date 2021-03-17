#!/bin/bash

if [ $# -lt 2 ];then
	echo -e '\033[1;91m  No arguments where given\033[00m'
	echo "Please provide 'k' and type of consistency (l,e)"
	echo "e.g. ./run_local.sh 10 3 l"
	exit 0
fi

for node in node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
		ssh user@$node "~/Distributed-NTUA/python3 server.py -p 5000 -k $1 -c $2 && exit"
		ssh user@$node "~/Distributed-NTUA/python3 server.py -p 5000 -k $1 -c $2 && exit"
		echo -e '\033[1;91m  Raised 2 servers\033[00m' $node
done
