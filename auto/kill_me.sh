#!/bin/bash
echo "I am $HOSTNAME and I am Killing all my nodes"
ps aux |grep python |awk '{print $2}' |xargs kill
