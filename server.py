import os
import sys
import hashlib
import json
from flask import Flask, request
import requests
from chord import *
import config
from utils.colorfy import *
import globs
import ends
import threading
import time
app = Flask(__name__)

@app.route('/',methods = ['GET'])												# root directory (useless)
def home():
	return "my name is ToyChord"


@app.route(ends.info ,methods = ['GET'])										# cli (client) operation info
def cli_info():
	return globs.my_id + " " + globs.my_ip + " " + globs.my_port


@app.route(ends.c_overlay ,methods = ['GET'])									# cli (client) operation network overlay
def cli_over():
	return client_overlay()

@app.route(ends.c_depart ,methods = ['GET'])									# cli (client) operation depart
def cli_depart():
	return cli_depart_func()

@app.route(ends.n_depart ,methods = ['POST'])									# cli (client) operation depart
def chord_depart():
	data = request.get_json()
	print(data)
	return chord_depart_func(data)

@app.route(ends.c_insert ,methods = ['POST'])									# cli (client) operation insert
def cli_insert():
	pair = request.form.to_dict()
	globs.started_insert = True
	x = threading.Thread(target=insert_t ,args = [pair])
	x.start()
	while not(globs.got_insert_response):
		if config.vNDEBUG:
			print(yellow("Waiting for insert respose..."))
			time.sleep(0.1)
	globs.got_insert_response = False
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	return globs.q_responder + " " + globs.q_response
	x.join()

def insert_t(pair):
	return insert_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

@app.route(ends.c_delete ,methods = ['POST'])									# cli (client) operation delete
def cli_delete():
	pair = request.form.to_dict()
	globs.started_delete = True
	x = threading.Thread(target=delete_t ,args = [pair])
	x.start()
	while not(globs.got_delete_response):
		if config.vNDEBUG:
			print(yellow("Waiting for delete respose..."))
			time.sleep(0.1)
	globs.got_delete_response = False
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	return globs.q_responder + " " + globs.q_response
	x.join()

@app.route(ends.chain_insert ,methods = ['POST'])
def chain_insert():
	data = request.get_json()
	song_for_chain = data["song"]
	k = data["chain_length"]["k"]
	next_ID = globs.nids[1]["uid"]
	who_is = data["who"]
	self_ID = globs.my_id
	song_to_be_inserted = found(song_for_chain["key"])
	if(song_to_be_inserted):
		globs.songs.remove(song_to_be_inserted)
		if config.NDEBUG:
			print(yellow('Updating song: {}').format(song_to_be_inserted))
			print(yellow("To song: 	{}").format(song_for_chain))
			if config.vNDEBUG:
				print(yellow("My songs are now:"))
				print(globs.songs)
	globs.songs.append({"key":song_for_chain["key"], "value":song_for_chain["value"]}) # inserts the (updated) pair of (key,value)
	if config.NDEBUG:
		print(yellow('Inserted song: {}').format(song_for_chain))
		if config.vNDEBUG:
			print(yellow("My songs are now:"))
			print(globs.songs)
	if(k>1):
		r = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.chain_insert,json = {"who": {"uid" : data["who"]["uid"], "ip":data["who"]["ip"], "port" :data["who"]["port"]}, "song" : {"key":song_for_chain["key"], "value":song_for_chain["value"]}, "chain_length":{"k":k-1}})
		return r.text
	else:
		if globs.replication == "eventual":
			return song_for_chain
		elif globs.replication == "linear":
			try: # send the key of the song to the node who requested the insertion
				globs.last_replica_flag=False
				if who_is["uid"]==globs.my_id:
					globs.last_replica_flag=True
				result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_insert, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": song_for_chain})
				if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
					if config.NDEBUG:
						print("Got response from the node who requested the insertion of the song: " + yellow(result.text))
					return self_ID + song_for_chain["key"]
				else:
					print(red("node who requested the insertion of the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
					return "Bad status code: " + result.status_code
			except:
				print(red("node who requested the insertion of the song dindnt respond at all"))
				return "Exception raised node who requested the insertion of the song dindnt respond"
		else:
			print("Not eventual, Not linear")
			return "something is going wrong"
			#return self_ID + song_for_chain["key"]

@app.route(ends.chain_delete ,methods = ['POST'])
def chain_delete():
	data = request.get_json()
	song_for_chain = data["song"]
	k = data["chain_length"]["k"]
	who_is = data["who"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	song_to_be_deleted = found(song_for_chain["key"])
	if(song_to_be_deleted):
		globs.songs.remove(song_to_be_deleted)
		if config.NDEBUG:
			print(yellow('Deleted song: {}').format(song_for_chain))
			if config.vNDEBUG:
				print(yellow("My songs are now:"))
				print(globs.songs)
		value = song_to_be_deleted["value"]
	else:
		if config.NDEBUG:
			print(yellow('Cant find song: {}').format(song_for_chain))
			print(yellow('Unable to delete'))
			if config.vNDEBUG:
				print(yellow("My songs are now:"))
				print(globs.songs)
		value = "@!@"
	if(k!=1):
		r = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.chain_delete,json = {"who": {"uid" : data["who"]["uid"], "ip":data["who"]["ip"], "port" :data["who"]["port"]}, "song" : {"key":song_for_chain["key"]}, "chain_length":{"k":(k-1)}})
		return r.text
	else:
		if globs.replication == "eventual":
			return song_for_chain["key"]
		elif globs.replication == "linear":
			try: # send the key of the song to the node who requested the insertion
				globs.last_replica_flag=False
				if who_is["uid"]==globs.my_id:
					globs.last_replica_flag=True

				result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_delete, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song":{"key":song_for_chain["key"],"value":value}})
				if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
					if config.NDEBUG:
						print("Got response from the node who requested the insertion of the song: " + yellow(result.text))
					return self_ID + value
				else:
					print(red("node who requested the insertion of the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
					return "Bad status code: " + result.status_code
			except:
				print(red("node who requested the insertion of the song dindnt respond at all"))
				return "Exception raised node who requested the insertion of the song dindnt respond"
		else:
			print("Not eventual, Not linear")
			return "something is going wrong"
			#return self_ID + song_for_chain["key"]

@app.route(ends.chain_query ,methods = ['POST'])
def chain_query():
	data = request.get_json()
	song_for_chain = data["song"]
	who_is = data["who"]
	#k = data[chain_length]["k"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id

	song_to_be_found = found(song_for_chain["key"])

	if(song_to_be_found and globs.replication == "linear"):
		if config.NDEBUG:
			print(yellow('Found song: {}').format(song_to_be_found))
			print("Sending the song to the next probable node who may have it and waiting for response...")
		r = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.chain_query,json = {"who": {"uid" : data["who"]["uid"], "ip":data["who"]["ip"], "port" :data["who"]["port"]}, "song" : {"key":song_for_chain["key"]}})
		if(r.text == "last_replica"):
			globs.last_replica_flag=False
			if who_is["uid"]==globs.my_id:
				globs.last_replica_flag=True
			try: # send the value or "@!@" (if the sond doesnt exist) to the node who requested it
				result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_query, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": {"key": song_for_chain["key"],"value": song_to_be_found["value"]}})
				if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
					if config.NDEBUG:
						print("Got response from the node who requested the song: " + yellow(result.text))
					return self_ID + song_to_be_found["value"]
				else:
					print(red("node who requested the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
					return "Bad status code: " + result.status_code
			except:
				print(red("node who requested the song dindnt respond at all"))
				return "Exception raised node who requested the song dindnt respond"
		else:
			return self_ID + song_to_be_found["value"]
	else: # couldnt find song
		if config.NDEBUG:
			print(yellow('Cant find song: {}').format(song_for_chain))
			print("Informing the previous node who requested it that the last replica of song is in in him and waiting for response...")
		return "last_replica"

def delete_t(pair):
	return delete_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})


@app.route(ends.c_query ,methods = ['POST'])									# cli (client) operation query
def cli_query():
	pair = request.form.to_dict()
	globs.started_query = True
	x = threading.Thread(target=query_t ,args = [pair])
	x.start()
	while not(globs.got_query_response):
		if config.vNDEBUG:
			print(yellow("Waiting for query respose..."))
			time.sleep(0.1)
	globs.got_query_response = False
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	return globs.q_responder + " " + globs.q_response
	x.join()

def query_t(pair):
	return query_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

@app.route(ends.c_query_star ,methods = ['GET'])								# cli (client) operation query *
def cli_query_star():
	globs.started_query_star = True
	x = threading.Thread(target=query_star_t ,args = [])
	x.start()
	while not(globs.got_query_star_response):
		if config.vNDEBUG:
			print(yellow("Waiting for query_star respose..."))
			time.sleep(0.1)
	globs.got_query_star_response = False
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	return globs.q_star_response
	x.join()

def query_star_t():
	initial_dict = {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}
	initial_dict["song"] = globs.songs
	dict_to_send = {"res": []}
	dict_to_send["res"].append(initial_dict)
	return query_star_song(dict_to_send)


@app.route(ends.n_overlay ,methods = ['POST'])									# chord operation network overlay
def chord_over():
	r_node = request.form.to_dict()
	return node_overlay(r_node)


@app.route(ends.n_insert ,methods = ['POST'])									# chord operation insert(key.value)
def chord_insert():
	result = request.get_json()
	return insert_song(result)

@app.route(ends.n_delete ,methods = ['POST'])									# chord operation delete(key)
def chord_delete():
	result = request.get_json()
	return delete_song(result)

@app.route(ends.n_query ,methods = ['POST'])									# chord operation query(key)
def chord_query():
	result = request.get_json()
	return query_song(result)

@app.route(ends.n_query_star ,methods = ['POST'])								# chord operation query *
def chord_query_star():
	result = request.get_json()
	return query_star_song(result)

@app.route(ends.n_update_peers ,methods = ['POST'])								# update(nodeID)
def chord_updateList():
	new_neighbours = request.get_json()
	return node_update_list(new_neighbours)


@app.route(ends.b_join ,methods = ['POST'])										# join(nodeID)
def boot_join():
	if globs.boot:
		new_node = request.form.to_dict()
		return bootstrap_join_func(new_node)
	else:
		print(red("You are not authorized to do this shitt...Therefore you are now DEAD"))
		exit(0)

@app.route(ends.chord_join_procedure,methods = ['POST'])										# join(nodeID)
def chord_join_procedure():
	print(red("Chord join procedure OK!"))
	if config.NDEBUG:
		print("chord_join_procedure is staring...")
	res = request.get_json()

	prev = res["prev"]
	next = res["next"]
	node_number = res["length"]
	node_list = []

	globs.nids.append({"uid": prev["uid"], "ip": prev["ip"], "port": prev["port"]})
	globs.nids.append({"uid": next["uid"], "ip": next["ip"], "port": next["port"]})
	if config.NDEBUG:
		print(yellow("Previous Node:"))
		print(globs.nids[0])
		print(yellow("Next Node:"))
		print(globs.nids[1])

	if globs.k <= node_number:
		if config.NDEBUG:
			print("Node list creation is starting...")
		data = {"node_list":node_list,"k":globs.k, "new_id":globs.my_id}
		node_list_json = chord_join_list_func(data)
		node_list = node_list_json["node_list"]
		if config.NDEBUG:
			print("Node list created: ",node_list)

		data = {"node_list":node_list,"new_id":globs.my_id}
		chord_join_update_post_func(data)

	if config.NDEBUG:
		print("Join of node completed - Overlay to check")

	return "Join Completed"

@app.route(ends.chord_join_update ,methods = ['POST'])									# depart(nodeID)
def chord_join_update():
	res = request.get_json()
	return chord_join_update_func(res)
	
@app.route(ends.chord_join_list ,methods = ['POST'])									# depart(nodeID)
def chord_join_list():
	data = request.get_json()
	return chord_join_list_func(data)

@app.route(ends.b_depart ,methods = ['POST'])									# depart(nodeID)
def boot_depart():
	d_node = request.form.to_dict()
	return boot_depart_func(d_node)

@app.route(ends.b_list ,methods = ['GET'])										# send nodesList
def boot_sendList():
	return boot_send_nodes_list()

def server():
	print("\n")
	if len(sys.argv) < 3:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
	if sys.argv[1] in ("-p", "-P"):
		globs.my_port = sys.argv[2]
	globs.my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	if len(sys.argv) == 4 and sys.argv[3] in ("-b", "-B"):
		print("I am the Bootstrap Node with ip: " + yellow(globs.my_ip) + " about to run a Flask server on port "+ yellow(globs.my_port))
		globs.my_id = hash(globs.my_ip + ":" + globs.my_port)
		print("and my unique id is: " + green(globs.my_id))
		globs.boot = True
		globs.mids.append({"uid":globs.my_id, "ip":globs.my_ip, "port":globs.my_port})	#boot is the first one to enter the list
		globs.nids.append({"uid":globs.my_id, "ip":globs.my_ip, "port":globs.my_port})	# initialy boot is the previous node of himself
		globs.nids.append({"uid":globs.my_id, "ip":globs.my_ip, "port":globs.my_port})	# initialy boot is the next node of himself
	else:
		globs.boot = False
		print("I am a normal Node with ip: " + yellow(globs.my_ip) + " about to run a Flask server on port "+ yellow(globs.my_port))
		globs.my_id = hash(globs.my_ip + ":" + globs.my_port)
		print("and my unique id is: " + green(globs.my_id))
		x = threading.Thread(target=node_initial_join ,args = [])
		x.start()

	print("\n\n")
	app.run(host= globs.my_ip, port=globs.my_port,debug = True, use_reloader=False)


if __name__ == '__main__':
	server()
