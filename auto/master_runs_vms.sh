#!/bin/bash

if [ $# -lt 3 ];then
	echo -e '\033[1;91m  No arguments where given\033[00m'
	echo "Please provide 'k' and type of consistency (l,e) and node yoy wish to raise"
	echo "e.g. ./run_local.sh 10 3 l"
	exit 0
fi

echo -e '\033[1;91m  Inside node:\033[00m' $3
ssh user@$3 "python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 && exit"
ssh user@$3 "python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2 && exit"
echo -e '\033[1;91m  Raised 2 servers\033[00m' $3
