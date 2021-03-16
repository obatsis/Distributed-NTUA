#!/bin/bash

gnome-terminal -- bash -c "./server_local.sh $1 $2 $3"
gnome-terminal -- bash -c "./cli_local.sh $1"

# declare -i x=355
# declare -i y=355
# gnome-terminal --geometry=20x10+$((0*$x))+0 -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((1*$x))+0 -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((2*$x))+0 -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((3*$x))+0 -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"

# gnome-terminal --geometry=20x10+$((0*$x))+$((1*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((1*$x))+$((1*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((2*$x))+$((1*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((3*$x))+$((1*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"

# gnome-terminal --geometry=20x10+$((0*$x))+$((2*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
# gnome-terminal --geometry=20x10+$((1*$x))+$((2*$y)) -- bash -c "python ~/Distributed-NTUA/cli_etimo_apo_pliroforiaka.py"
