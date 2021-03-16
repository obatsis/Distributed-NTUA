#!/bin/bash

for (( i=0; i< $1; i++))
do
  echo "Looping ... number $i"
  gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/cli_ui.py -p 500$i; exec bash"
done
