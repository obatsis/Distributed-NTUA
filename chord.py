import requests
from utils.colorfy import *
import globs
import config


def node_initial_join():
	if not globs.boot:
		if config.NDEBUG:
			print(yellow("\natempting to join the Chord..."))
		try:
			response = requests.post(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + "/boot/join", data = {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port})
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

	response_p = requests.post(config.ADDR + prev["ip"] + ":" + prev["port"] + "/chord/updatePeersList", json = {"prev" : prev_of_prev, "next": new_node})
	if response_p.status_code == 200 and response_p.text == "new neighbours set":
		if config.BDEBUG:
			print(blue("Updated previous neighbour successfully"))
	else :
		print(RED("Something went wrong while updating previous node list"))
	response_n = requests.post(config.ADDR + next["ip"] + ":" + next["port"] + "/chord/updatePeersList", json = {"prev" : new_node, "next": next_of_next})
	if response_n.status_code == 200 and response_n.text == "new neighbours set":
		if config.BDEBUG:
			print(blue("Updated next neighbour successfully"))
	else :
		print(RED("Something went wrong while updating next node list"))

	return prev["uid"] + " " + prev["ip"] + " " + prev["port"] + " " + next["uid"] + " " + next["ip"] + " " + next["port"]

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

def client_overlay():
	try:
		globs.started_overlay = True	# i am the node starting the overlay
		# hit the endpoint /chord/overlay of your next node
		response = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + "/chord/overlay", data = {"uid": globs.my_id, "ip": globs.my_ip, "port": globs.my_port})
		if response.status_code == 200:
			return globs.my_ip + ":" + globs.my_port + " -> " + response.text
		else :
			return "Something went wrong while trying to start the overlay.... Next node doesnt return properly"
	except:
	  return "Node " + globs.nids[1]["uid"] + "  " + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + " is not responding"

def node_overlay(r_node):
	if globs.started_overlay: # it means i am the node who started the overlay
		globs.started_overlay = False
		return globs.my_ip + ":" + globs.my_port
	if config.NDEBUG:
		print("got a request for overlay from")
		print(yellow(r_node))
	try: # hit the endpoint /chord/overlay of your next node
		if config.NDEBUG:
			print("sending request for overlay to")
			print(yellow(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + "/chord/overlay"), )
		response = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + "/chord/overlay", data = {"uid": globs.my_id, "ip": globs.my_ip, "port": globs.my_port})
		if response.status_code == 200:
				return globs.my_ip + ":" + globs.my_port + " -> " + response.text
		else :
				return "Something went wrong while trying to start the overlay.... Next node doesent return properly"
	except:
	  return "Node " + globs.nids[1]["uid"] + "  " + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + " is not responding"
