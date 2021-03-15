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
global still_on_chord	# flag that becomes (and stays) false when a node departs (used to prevent unwanted operation from a departed node)
still_on_chord = True

# Songs global variables
#-------------------------------------------------------------------------------------------------------
global songs	# list of songs saved on a node (contains dicts that look like: {"key": "Song-title, "value": "some value"})
songs = []

#-------------------------------------------------------------------------------------------------------
# variables for async receiving
global started_overlay	# flag that becomes true if a node starts an overlay operation (when the operation finishes, it becomes false arain)
started_overlay = False
global started_query		# flag that becomes true if a node starts a query (when the operation finishes, it becomes false arain)
started_query = False
global started_query_star	# flag that becomes true if a node starts a query *(when the operation finishes, it becomes false arain)
started_query_star = False
global started_delete		# flag that becomes true if a node starts a delete (when the operation finishes, it becomes false arain)
started_delete = False
global started_insert		# flag that becomes true if a node starts an insert (when the operation finishes, it becomes false arain)
started_insert = False

global got_overlay_response
got_overlay_response = False
global got_query_response
got_query_response = False
global got_query_star_response
got_query_star_response = False
global got_delete_response
got_delete_response = False
global got_insert_response
got_insert_response = False
global q_response
global q_star_response
global q_responder

global consistency	# 'linear' or 'eventual' or 'none'
consistency = "linear"

global k	# must be < number of nodes
k = 5

global last_replica_flag
last_replica_flag=False
