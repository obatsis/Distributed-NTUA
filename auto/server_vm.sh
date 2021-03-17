#!/bin/bash
# hs=$HOSTNAME
#
# if [ $hs = "master" ]; then
# 	python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 -b &
# else
# 	python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 &
# fi
# sleep 1
# python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2 &
# # python3 ~/Distributed-NTUA/cli_ui.py -p 5000

# $1 is k (replication factor)
# $2 is consistency type (l,c)
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
		PROMPT_COMMAND='echo -ne "\033]0;master 5000\007"'
		gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 -b; exec bash'"
		PROMPT_COMMAND='echo -ne "\033]0;master 5001\007"'
		gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2; exec bash'"
	# ssh user@$node "/home/user/Distributed-NTUA/auto/server_vm.sh $1 $2 && exit"
	else
		gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 '~/Distributed-NTUA/auto/master_runs_vms0.sh $1 $2 $node; exec bash'"
		gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 '~/Distributed-NTUA/auto/master_runs_vms1.sh $1 $2 $node; exec bash'"
		# gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'ssh user@$node "~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2; exec bash"'"
		# gnome-terminal --tab -- bash -c "sshpass -p vmm ssh user@83.212.74.75 'ssh user@$node "~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2; exec bash"'"
	fi
done

# ssh user@$node "/home/user/Distributed-NTUA/auto/server_vm.sh $1 $2 && exit"

# for (( i=0; i< $1; i++))
# do
# 	echo "Looping ... number $i"
# 	if (($i == 0)); then
# 		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 5000 -k $2 -c $3 -b; exec bash"
# 	else
# 		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 500$i -k $2 -c $3; exec bash"
# 	fi
# done
