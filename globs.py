# This file contains all global variables that represent the state of ith node
# in the network (e.g. Node_PeersList, Master_PeersList, ID, IP, PORT, ...)
global boot	# true if node is bootstrap
global mids
mids = []	# list of dicts, decending uids
global nids
nids = []	# list of dicts, first element is the previous node and second element is the next node
global my_id
global my_ip
global my_port
global started_overlay
started_overlay = False
global still_on_chord
still_on_chord = True

#-------------------------------------------------------------------------------------------------------
global songs
songs = []
