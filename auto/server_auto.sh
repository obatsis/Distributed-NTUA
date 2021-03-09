#!/bin/bash

gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 5000 -b; exec bash"

for i in $(seq 1 $1)
do
  echo "Looping ... number $i"
  gnome-terminal --tab -- bash -c "python ~/Distributed-NTUA/server.py -p 500$i; exec bash"
done