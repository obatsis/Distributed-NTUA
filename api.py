import requests
address = 'http://localhost:'


# here we must have a list or something to save the next and prev Node
# we must save both ip and port in order to be compatible with the vms when the time comes
# global boot, my_ip, my_id, nids, mids
mids = []
next_node = 0
prev_node = 0

def insert_song(dict):
	return "inserted " + dict["val"]
