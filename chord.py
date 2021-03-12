import requests
from utils.colorfy import *
import globs
import config
import ends
import hashlib
import json
import time
from threading import Thread
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

		response_p = requests.post(config.ADDR + prev["ip"] + ":" + prev["port"] + ends.n_update_peers, json = {"prev": prev_of_prev, "next": next})
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


def boot_send_nodes_list():
	if globs.boot:
		res = ''
		for node in globs.mids:
			res += node["ip"] + ":" + node["port"] + " "
		print(yellow("Sending nodes: ") + res)
		return res
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
		  return "Node " + globs.nids[1]["uid"] + " is not responding"

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
		  return "Node " + globs.nids[1]["uid"] + " is not responding"

#  End Overlay Functions
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Song Functions

def hash(key):
	return hashlib.sha1(key.encode('utf-8')).hexdigest()

def found(key):
	for item in globs.songs:
		if item['key'] == key:
			return item

def insert_song(args):
	song = args["song"]
	who_is = args["who"]
	if who_is["uid"] != globs.my_id and globs.started_insert:
		# i am the node who requested the insertion of the song and i am here because the node who has the song sent it to me
		if config.NDEBUG:
			print(yellow("Got response directly from the source: ") + who_is["uid"])
			print(yellow("and it contains: ") + str(song))
			print(yellow("sending confirmation to source node"))
		globs.q_responder = who_is["uid"]
		globs.q_response = song["key"]
		globs.started_insert = False
		globs.got_insert_response = True
		return globs.my_id + " " + song["key"]

	hashed_key = hash(song["key"])
	if config.NDEBUG:
		print(yellow("Got request to insert song: {}").format(song))
		print(yellow("From node: ") + who_is["uid"])
		print(yellow("Song Hash: ") + hashed_key)
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	who = 1
	if previous_ID > self_ID and next_ID > self_ID:
		who = 0	# i have the samallest id
	elif previous_ID < self_ID and next_ID < self_ID:
		who = 2 # i have the largest id

	if(hashed_key > previous_ID and hashed_key <= self_ID and who != 0) or (hashed_key > previous_ID and hashed_key > self_ID and who == 0) or (hashed_key <= self_ID and who == 0):
		# song goes in me
		song_to_be_inserted = found(song["key"])
		if(song_to_be_inserted):
			globs.songs.remove(song_to_be_inserted)
			if config.NDEBUG:
				print(yellow('Updating song: {}').format(song_to_be_inserted))
				print(yellow("To song: 	{}").format(song))
				if config.vNDEBUG:
					print(yellow("My songs are now:"))
					print(globs.songs)
		globs.songs.append({"key":song["key"], "value":song["value"]}) # inserts the (updated) pair of (key,value)
		if config.NDEBUG:
			print(yellow('Inserted song: {}').format(song))
			if config.vNDEBUG:
				print(yellow("My songs are now:"))
				print(globs.songs)
		if globs.started_insert:# it means i requested the insertion of the song, and i am responsible for it
			globs.q_response = song["key"]
			globs.q_responder = who_is["uid"]
			globs.started_insert = False
			globs.got_insert_response = True
			if config.NDEBUG:
				print(cyan("Special case ") + "it was me who made the request and i also have the song")
				print(yellow("Returning to myself..."))
			return "sent it to myself"
		try: # send the key of the song to the node who requested the insertion
			result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_insert, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": song})
			if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
				if config.NDEBUG:
					print("Got response from the node who requested the insertion of the song: " + yellow(result.text))
				return self_ID + song["key"]
			else:
				print(red("node who requested the insertion of the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
				return "Bad status code: " + result.status_code
		except:
			print(red("node who requested the insertion of the song dindnt respond at all"))
			return "Exception raised node who requested the insertion of the song dindnt respond"


	elif((hashed_key > self_ID and who != 0) or (hashed_key > self_ID and hashed_key < previous_ID and who == 0) or (hashed_key <= next_ID and who !=0) or (hashed_key <= previous_ID and hashed_key > next_ID and who == 2)):
		# forward song to next
		if config.NDEBUG:
			print(yellow('forwarding to next..'))
		try:
			result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_insert, json = {"who": who_is, "song": song})
			if result.status_code == 200:
				if config.NDEBUG:
					print("Got response from next: " + yellow(result.text))
				return result.text
			else:
				print(red("Something went wrong while trying to forward insert to next"))
				return "Bad status code: " + result.status_code
		except:
			print(red("Next is not responding to my call..."))
			return "Exception raised while forwarding to next"
		return self_ID
	else :
		print(red("The key hash didnt match any node...consider thinking again about your skills"))
		return "Bad skills"

def delete_song(args):
	song = args["song"]
	who_is = args["who"]
	if who_is["uid"] != globs.my_id and globs.started_delete:
		# i am the node who requested the deletion of the song and i am here because the node who has the song sent it to me
		if config.NDEBUG:
			print(yellow("Got response directly from the source: ") + who_is["uid"])
			print(yellow("and it contains: ") + str(song))
			print(yellow("sending confirmation to source node"))
		globs.q_responder = who_is["uid"]
		globs.q_response = song["key"]
		globs.started_delete = False
		globs.got_delete_response = True
		return globs.my_id + " " + song["key"]

	hashed_key = hash(song["key"])
	if config.NDEBUG:
		print(yellow("Got request to delete song: {}").format(song))
		print(yellow("From node: ") + who_is["uid"])
		print(yellow("Song Hash: ") + hashed_key)
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	who = 1
	if previous_ID > self_ID and next_ID > self_ID:
		who = 0	# i have the samallest id
	elif previous_ID < self_ID and next_ID < self_ID:
		who = 2 # i have the largest id
	if(hashed_key > previous_ID and hashed_key <= self_ID and who != 0) or (hashed_key > previous_ID and hashed_key > self_ID and who == 0) or (hashed_key <= self_ID and who == 0):
		# song is in me
		song_to_be_deleted = found(song["key"])
		if(song_to_be_deleted):
			globs.songs.remove(song_to_be_deleted)
			if config.NDEBUG:
				print(yellow('Deleted song: {}').format(song))
				if config.vNDEBUG:
					print(yellow("My songs are now:"))
					print(globs.songs)
			value = song_to_be_deleted["key"]
		else:
			if config.NDEBUG:
				print(yellow('Cant find song: {}').format(song))
				print(yellow('Unable to delete'))
				if config.vNDEBUG:
					print(yellow("My songs are now:"))
					print(globs.songs)
			value = "@!@"
		if globs.started_delete:# it means i requested the deletion of the song, and i am responsible for it
			globs.q_response = song_to_be_deleted["value"] if song_to_be_deleted else "@!@"
			globs.q_responder = who_is["uid"]
			globs.started_delete = False
			globs.got_delete_response = True
			if config.NDEBUG:
				print(cyan("Special case ") + "it was me who made the request and i also have the song")
				print(yellow("Returning to myself..."))
			return "sent it to myself"
		try: # send the value (key of the song) or "@!@" (if the sond doesnt exist) to the node who requested the deletion
			result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_delete, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": {"key": value}})
			if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
				if config.NDEBUG:
					print("Got response from the node who requested the deletion of the song: " + yellow(result.text))
				return self_ID + value
			else:
				print(red("node who requested the deletion of the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
				return "Bad status code: " + result.status_code
		except:
			print(red("node who requested the deletion of the song dindnt respond at all"))
			return "Exception raised node who requested the deletion of the song dindnt respond"

	elif((hashed_key > self_ID and who != 0) or (hashed_key > self_ID and hashed_key < previous_ID and who == 0) or (hashed_key <= next_ID and who !=0) or (hashed_key <= previous_ID and hashed_key > next_ID and who == 2)):
		# forward delete to next
		if config.NDEBUG:
			print(yellow('forwarding delete to next..'))
		try:
			result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_delete, json = {"who": who_is, "song": {"key": song["key"]}})
			if result.status_code == 200:
				if config.NDEBUG:
					print("Got response from next: " + yellow(result.text))
				return result.text
			else:
				print(red("Something went wrong while trying to forward delete to next"))
				return "Bad status code: " + result.status_code
		except:
			print(red("Next is not responding to my call..."))
			return "Exception raised while forwarding delete to next"
	else :
		print(red("The key hash didnt match any node...consider thinking again about your skills"))
		return "Bad skills"

def query_song(args):
	song = args["song"]
	who_is = args["who"]
	if who_is["uid"] != globs.my_id and globs.started_query:
		# i am the node who requested the song and i am here because the node who has the song sent it to me
		if config.NDEBUG:
			print(yellow("Got response directly from the source: ") + who_is["uid"])
			print(yellow("and it contains: ") + str(song))
			print(yellow("sending confirmation to source node"))
		globs.q_responder = who_is["uid"]
		globs.q_response = song["key"]
		globs.started_query = False
		globs.got_query_response = True
		return globs.my_id + " " + song["key"]

	hashed_key = hash(song["key"])
	if config.NDEBUG:
		print(yellow("Got request to search for song: {}").format(song))
		print(yellow("From node: ") + who_is["uid"])
		print(yellow("Song Hash: ") + hashed_key)
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	who = 1
	if previous_ID > self_ID and next_ID > self_ID:
		who = 0	# i have the samallest id
	elif previous_ID < self_ID and next_ID < self_ID:
		who = 2 # i have the largest id

	if(hashed_key > previous_ID and hashed_key <= self_ID and who != 0) or (hashed_key > previous_ID and hashed_key > self_ID and who == 0) or (hashed_key <= self_ID and who == 0):
		# song is in me
		song_to_be_found = found(song["key"])

		if globs.started_query:# it means i requested the song, and i am responsible for it
			globs.q_response = song_to_be_found["value"] if song_to_be_found else "@!@"
			globs.q_responder = who_is["uid"]
			globs.started_query = False
			globs.got_query_response = True
			if config.NDEBUG:
				print(cyan("Special case ") + "it was me who made the request and i also have the song")
				print(yellow("Returning to myself..."))
			return "sent it to myself"

		if song_to_be_found:# found the song
			if config.NDEBUG:
				print(yellow('Found song: {}').format(song_to_be_found))
				print("Sending the song to the node who requested it and waiting for response...")
			value = song_to_be_found["value"]
		else: # couldnt find song
			if config.NDEBUG:
				print(yellow('Cant find song: {}').format(song))
				print("Informing the node who requested it that song doesnt exist and waiting for response...")
			value = "@!@"
		try: # send the value or "@!@" (if the sond doesnt exist) to the node who requested it
			result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_query, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": {"key": value}})
			if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
				if config.NDEBUG:
					print("Got response from the node who requested the song: " + yellow(result.text))
				return self_ID + value
			else:
				print(red("node who requested the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
				return "Bad status code: " + result.status_code
		except:
			print(red("node who requested the song dindnt respond at all"))
			return "Exception raised node who requested the song dindnt respond"

	elif((hashed_key > self_ID and who != 0) or (hashed_key > self_ID and hashed_key < previous_ID and who == 0) or (hashed_key <= next_ID and who !=0) or (hashed_key <= previous_ID and hashed_key > next_ID and who == 2)):
		# forward query to next
		if config.NDEBUG:
			print(yellow('forwarding query to next..'))
		try:
			result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_query, json = {"who": who_is, "song": song})
			if result.status_code == 200:
				if config.NDEBUG:
					print("Got response from next: " + yellow(result.text))
				return result.text
			else:
				print(red("Something went wrong while trying to forward query to next"))
				return "Bad status code: " + result.status_code
		except:
			print(red("Next is not responding to my call..."))
			return "Exception raised while forwarding query to next"

	else :
		print(red("The key hash didnt match any node...consider thinking again about your skills"))
		return "Bad skills"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class my_thread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
