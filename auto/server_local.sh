#!/bin/bash

for (( i=0; i< $1; i++))
do
	echo "Looping ... number $i"
	if (($i == 0)); then
		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 5000 -k $2 -c $3 -b; exec bash"
	else
		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 500$i -k $2 -c $3; exec bash"
	fi
done
