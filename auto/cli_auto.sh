#!/bin/bash

# for i in $(seq 1 $1)
# do
#   echo "Looping ... number $i"
#   gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/cli_ui.py -p 500$i; exec bash"
# done

for (( i=0; i< $1; i++))
do
	echo "Looping ... number $i"
	if (($i == 0)); then
		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/cli_ui.py -p 5000; exec bash"
	else
		gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/cli_ui.py -p 500$i; exec bash"
	fi
done