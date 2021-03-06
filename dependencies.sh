#!/bin/bash

# quick alias for python

FILE=~/.bash_aliases
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
		if [[ `tail -n 1 $FILE` == "alias pip='pip3'" ]] ; then
			echo " -------- aliases already in place!";
		else
				echo " -------- adding needed aliases..."
				echo -e "\n#python aliases \nalias python='python3' \nalias pip='pip3'" >> $FILE
		fi
else
    echo "$FILE does not exist."
		touch ~/.bash_aliases && echo "creating file $FILE"
		echo " -------- adding needed aliases..."
		echo -e "\n#python aliases \nalias python='python3' \nalias pip='pip3'" >> $FILE
fi


# -e is for appending lines
echo " -------- installing dependecies -------- "
apt-get install python3-venv
pip3 install Flask
pip3 install requests
pip3 install PyInquirer
