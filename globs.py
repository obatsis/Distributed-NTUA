# This file contains all global variables that represent the state of ith node
# in the network (e.g. Node_PeersList, Master_PeersList, ID, IP, PORT, ...)
# as well as variables conserning the songs saved in each node
#-------------------------------------------------------------------------------------------------------
# General
global boot		# true if node is bootstrap
global mids
mids = []		# list of dicts, decending uids
global nids
nids = []		# list of dicts, first element is the previous node and second element is the next node
global my_id	# uniqu id of node (result of hashing ip:port)
global my_ip	# ip of node
global my_port	# port that Flask is listening
global started_overlay	# flag that becomes true if a node starts an overlay operation (when the operation finishes, it becomes false arain)
started_overlay = False
global still_on_chord	# flag that becomes (and stays) false when a node departs (used to prevent unwanted operation from a departed node)
still_on_chord = True
first_on_query = False

#-------------------------------------------------------------------------------------------------------
# Songs global variables
global songs	# list of songs saved on a node (contains dicts that look like: {"key": "Song-title, "value": "some value"})
songs = []
