import requests
from utils.colorfy import *
import globs
import config
import ends
import hashlib
import json

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Node Functions
def node_initial_join():
	if globs.still_on_chord:
		if not globs.boot:
			if config.NDEBUG:
				print(yellow("\natempting to join the Chord..."))
			try:
				response = requests.post(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + ends.b_join , data = {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port})
				if response.status_code == 200:
					res = response.text.split(" ")
					globs.nids.append({"uid": res[0], "ip": res[1], "port": res[2]})
					globs.nids.append({"uid": res[3], "ip": res[4], "port": res[5]})
					if config.NDEBUG:
						print(yellow("Joined Chord saccessfully!!"))
						print(yellow("Previous Node:"))
						print(globs.nids[0])
						print(yellow("Next Node:"))
						print(globs.nids[1])
				else:
					print("Something went wrong!!  status code: " + red(response.status.code))
					print(red("\nexiting..."))
					exit(0)
			except:
				print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
				print(red("\nexiting..."))
				exit(0)


def bootstrap_join_func(new_node):
	candidate_id = new_node["uid"]
	if config.BDEBUG:
		print(blue(candidate_id) + "  wants to join the Chord with ip:port " + blue(new_node["ip"] + ":" + new_node["port"]))
	for idx, ids in enumerate(globs.mids):
		if candidate_id < ids["uid"]:
			globs.mids.insert(idx, new_node)
			break
		elif idx == len(globs.mids)-1:
			globs.mids.append(new_node)
			break
	new_node_idx = globs.mids.index(new_node)
	if config.vBDEBUG:
		print(blue(globs.mids))
		print(blue("new node possition in globs.mids: " + str(new_node_idx)))
	prev_of_prev 	= globs.mids[new_node_idx-2] if new_node_idx >= 2 else (globs.mids[-1] if new_node_idx >= 1 else globs.mids[-2])
	prev 			= globs.mids[new_node_idx-1] if new_node_idx >= 1 else globs.mids[-1]
	next 			= globs.mids[new_node_idx+1] if new_node_idx < len(globs.mids)-1 else globs.mids[0]
	next_of_next 	= globs.mids[new_node_idx+2] if new_node_idx < len(globs.mids)-2 else (globs.mids[0] if new_node_idx < len(globs.mids)-1 else globs.mids[1])

	response_p = requests.post(config.ADDR + prev["ip"] + ":" + prev["port"] + ends.n_update_peers, json = {"prev" : prev_of_prev, "next": new_node})
	if response_p.status_code == 200 and response_p.text == "new neighbours set":
		if config.BDEBUG:
			print(blue("Updated previous neighbour successfully"))
	else :
		print(RED("Something went wrong while updating previous node list"))
	response_n = requests.post(config.ADDR + next["ip"] + ":" + next["port"] + ends.n_update_peers, json = {"prev" : new_node, "next": next_of_next})
	if response_n.status_code == 200 and response_n.text == "new neighbours set":
		if config.BDEBUG:
			print(blue("Updated next neighbour successfully"))
	else :
		print(RED("Something went wrong while updating next node list"))

	return prev["uid"] + " " + prev["ip"] + " " + prev["port"] + " " + next["uid"] + " " + next["ip"] + " " + next["port"]

def cli_depart_func():
	if globs.still_on_chord:
		globs.still_on_chord = False	# dont let him enter twice
		# sending a request to bootsrap saying i want to depart
		try:
			response = requests.post(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + ends.b_depart, data = {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port})
			if response.status_code == 200:
				if response.text == "you are ok to die":
					if config.NDEBUG:
						print(yellow("Bootsrap is aware of me leaving"))
						print(yellow("\nLeaving the Chord..."))
					return "Left the Chord"
				else :
					print(red("Something went wrong while trying to leave the Chord..."))
					print(yellow("Sorry but you are not allowed to leave."))
					print(yellow("Please contact your administrator."))
					return "Bootsrap doesnt let me leave"
			else :
				print(red("Bad status code from Bootsrap... Cant leave..."))
				return "Problem... Bad status code" + str(response.status_code)

		except:
			print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
			print(red("Cant realy do anything... I will wait"))
			return "Encountered a problem while trying to leave the Chord...\n Check if Bootstrap is up and running"



def boot_depart_func(d_node):
	if globs.boot:
		d_node_idx = globs.mids.index(d_node)

		if config.BDEBUG:
			print(blue("Got a request to remove node:"))
			print(d_node)
			if config.vBDEBUG:
				print(blue("Current Topology:"))
				print(blue(globs.mids))
				print(blue("leaving node possition in globs.mids: " + str(d_node_idx)))

		prev_of_prev 	= globs.mids[d_node_idx-2] if d_node_idx >= 2 else (globs.mids[-1] if d_node_idx >= 1 else globs.mids[-2])
		prev 			= globs.mids[d_node_idx-1] if d_node_idx >= 1 else globs.mids[-1]
		next 			= globs.mids[d_node_idx+1] if d_node_idx < len(globs.mids)-1 else globs.mids[0]
		next_of_next 	= globs.mids[d_node_idx+2] if d_node_idx < len(globs.mids)-2 else (globs.mids[0] if d_node_idx < len(globs.mids)-1 else globs.mids[1])

		response_p = requests.post(config.ADDR + prev["ip"] + ":" + prev["port"] + ends.n_update_peers, json = {"prev" : prev_of_prev, "next": next})
		if response_p.status_code == 200 and response_p.text == "new neighbours set":
			if config.BDEBUG:
				print(blue("Updated previous neighbour successfully"))
			p_ok = True
		else :
			print(RED("Something went wrong while updating previous node list"))
			p_ok = False

		response_n = requests.post(config.ADDR + next["ip"] + ":" + next["port"] + ends.n_update_peers, json = {"prev" : prev, "next": next_of_next})
		if response_n.status_code == 200 and response_n.text == "new neighbours set":
			if config.BDEBUG:
				print(blue("Updated next neighbour successfully"))
			n_ok = True
		else :
			print(RED("Something went wrong while updating next node list"))
			n_ok = False

		if n_ok and p_ok:
			del globs.mids[d_node_idx]
			if config.BDEBUG:
				print("Remooved Node: ", end = '')
				print(blue(d_node), end = '')
				print(" successfully!")
			return "you are ok to die"
		else:
			print(RED("Cannot remmove Node: "), end = '')
			print(blue(d_node), end = '')
			return "no"


def node_update_list(new_neighbours):
	globs.nids[0] = new_neighbours["prev"]
	globs.nids[1] = new_neighbours["next"]
	if config.NDEBUG:
		print(yellow("My neighbours have changed!"))
		print(yellow("NEW Previous Node:"))
		print(globs.nids[0])
		print(yellow("NEW Next Node:"))
		print(globs.nids[1])
	return "new neighbours set"


# End Node Functios
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Overlay Functions
def client_overlay():
	if globs.still_on_chord:
		globs.started_overlay = True	# i am the node starting the overlay
		try:
			# hit the endpoint /chord/overlay of your next node
			response = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_overlay, data = {"uid": globs.my_id, "ip": globs.my_ip, "port": globs.my_port})
			if response.status_code == 200:
				return globs.my_ip + ":" + globs.my_port + " -> " + response.text
			else :
				return "Something went wrong while trying to start the overlay   Next node doesnt return properly"
		except:
		  return "Node " + globs.nids[1]["uid"] + "  " + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + " is not responding"

def node_overlay(r_node):
	if globs.still_on_chord:
		if globs.started_overlay: # it means i am the node who started the overlay
			globs.started_overlay = False
			return globs.my_ip + ":" + globs.my_port
		if config.NDEBUG:
			print("got a request for overlay from")
			print(yellow(r_node))
		try: # hit the endpoint /chord/overlay of your next node
			if config.NDEBUG:
				print("sending request for overlay to")
				print(yellow(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_overlay), )
			response = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_overlay, data = {"uid": globs.my_id, "ip": globs.my_ip, "port": globs.my_port})
			if response.status_code == 200:
					return globs.my_ip + ":" + globs.my_port + " -> " + response.text
			else :
					return "Something went wrong while trying to start the overlay.... Next node doesent return properly"
		except:
		  return "Node " + globs.nids[1]["uid"] + "  " + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + " is not responding"

#  End Overlay Functions
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Song Functions

def hash(key):
	return hashlib.sha1(key.encode('utf-8')).hexdigest()

def found(songs_list, key):
	for item in songs_list:
		if item[0] == key:
			return(item)


def insert_song(args):
	print(args) # args is a pair of (key,value)
	hashed_key = hash(args["key"])
	command = 'insert'
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	if(hashed_key > previous_ID and hashed_key <= self_ID):
		item = found(globs.songs, args["key"])
		if(item): # update
			globs.songs.remove(item)
		globs.songs.append({"key":args["key"], "value":args["value"]}) # inserts the updated pair of (key,value)
		if config.NDEBUG:
			print('Updated!')
			print(globs.songs)
		return "Inserted by node" + self_ID
	elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
		item = found(globs.songs, args["key"])
		if(item): # update
			globs.songs.remove(item)
		globs.songs.append({"key":args["key"], "value":args["value"]}) # inserts the updated pair of (key,value)
		if config.NDEBUG:
			print('Updated!')
			print(globs.songs)
		return "Inserted by node" + self_ID
	elif(hashed_key > self_ID or hashed_key < previous_ID):
		if config.NDEBUG:
			print('forwarding..')
		tuple_load = {"key":args["key"], "value":args["value"]}
		result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_insert, data = tuple_load)
		# req = requests.get(url = 'http://' + next_ID + '/insert', params = tuple_load)
		return result.text
	print("Insersion from server is done!")


def delete_song(args):
	print(args) # args is a pair of (key,value)
	hashed_key = hash(args["key"])
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	command = 'delete'
	if(hashed_key > previous_ID and hashed_key <= self_ID):
		item = found(globs.songs, args["key"])
		if(item):
			globs.songs.remove(item)
		if config.NDEBUG:
			print('Deleted!')
			print(globs.songs)
		return "Removed by node" + self_ID
	elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
		item = found(globs.songs, args["key"])
		if(item):
			globs.songs.remove(item)
		if config.NDEBUG:
			print('Deleted!')
			print(globs.songs)
		return "Removed by node" + self_ID
	elif(hashed_key > self_ID or hashed_key < previous_ID):
		if config.NDEBUG:
			print('forwarding..')
		result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_delete, data = {"key": args["key"]})
		# req = requests.get(url = 'http://' + next_ID + '/delete', params = tuple_load)
		return result.text
	print("Deletion from server is done!")


def query_song(args):
	command = 'query'
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	if(node_in_chord == False):
		return 'NodeIsDown'
	if(args["key"] == '*'):
		return (json.dumps({'matrix_of_items':matrix_of_items}))
	else:
		hashed_key = hash(args["key"])
		# δεν θεωρω οτι το id ειναι χασαρισμενο...
		if(hashed_key > previous_ID and hashed_key < self_ID):
			item = found(globs.songs, args["key"])
			if config.NDEBUG:
				print('It is found..')
				print(item)
			return json.dumps(item)
		elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
			item = found(globs.songs, args["key"])
			if config.NDEBUG:
				print('It is found..')
				print(item)
			return json.dumps(item)
		elif(hashed_key > self_ID or hashed_key < previous_ID):
			if config.NDEBUG:
				print('forwarding..')
			tuple_load = {"key":args["key"]}
			result = requests.post(config.ADDR + globs.songs[1]["ip"] + ":" + globs.songs[1]["port"] + ends.n_query, data = tuple_load)
			# req = requests.get(url = 'http://' + next_ID + '/query', params = tuple_load)
			return result.text
