#!/bin/bash

dir="/home/user/Distributed-NTUA"
if [ -d "$dir" ]
then
	cd Distributed-NTUA
	echo "fetching..."
	git fetch
	echo "Pulling main from repo github.com:obatsis/Distributed-NTUA.git"
	git reset --hard HEAD
	git merge @{u}
else
	echo "Cloning repo github.com:obatsis/Distributed-NTUA.git"
	git clone https://github.com/obatsis/Distributed-NTUA.git
fi
