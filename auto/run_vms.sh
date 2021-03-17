#!/bin/bash

if [ $# -lt 2 ];then
	echo -e '\033[1;91m  No arguments where given\033[00m'
	echo "Please provide 'k' and type of consistency (l,e)"
	echo "e.g. ./run_local.sh 10 3 l"
	exit 0
fi

for node in master node1 node2 node3 node4
do
	echo -e '\033[1;91m  Inside node:\033[00m' $node
	if [ $node = "master" ]; then
		gnome-terminal --title="master 5000" --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 -b; exec bash'"
		gnome-terminal --title="master 5001" --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2; exec bash'"
	else
		gnome-terminal --title=$node" 5000" --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 '~/Distributed-NTUA/auto/master_runs_vms0.sh $1 $2 $node; exec bash'"
		gnome-terminal --title=$node" 5001" --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 '~/Distributed-NTUA/auto/master_runs_vms1.sh $1 $2 $node; exec bash'"
	fi
done
