#!/bin/bash
hs=$HOSTNAME

if [ $hs = "master" ]; then
	python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 -b &
else
	python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 &
fi
python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2 &
