#!/bin/bash
hs=$HOSTNAME

if [ $hs = "T460" ]; then
	gnome-terminal --tab -- bash -c "python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2 -b; exec bash"
else
	gnome-terminal --tab -- bash -c "python3 ~/Distributed-NTUA/server.py -p 5000 -k $1 -c $2; exec bash"
fi
gnome-terminal --tab -- bash -c "python3 ~/Distributed-NTUA/server.py -p 5001 -k $1 -c $2; exec bash"
