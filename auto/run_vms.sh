#!/bin/bash
# $1 is k (replication factor)
# $2 is consistency type (l,c)
if [ $# -lt 2 ];then
	echo -e '\033[1;91m  No arguments where given\033[00m'
	echo "Please provide 'k' and type of consistency (l,e)"
	echo "e.g. ./run_vms.sh 3 l"
	exit 0
fi
for node in master node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
	cd auto
	ssh user@$node "/home/user/Distributed-NTUA/auto/server_vm.sh $1 $2 && exit"
done
