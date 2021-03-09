#!/bin/bash

for i in $(seq 1 $1)
do
  echo "Looping ... number $i"
  gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/cli_ui.py -p 500$i; exec bash"
done