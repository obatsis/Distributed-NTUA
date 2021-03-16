import os
import sys
import hashlib
import json
from flask import Flask, request
import requests
from chord import *
from utils.colorfy import *
import utils.globs as globs
import utils.config as config
import utils.ends as ends
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
	globs.started_overlay = True
	x = threading.Thread(target=overlay_t ,args = [])
	x.start()
	while not(globs.got_overlay_response):
		if config.vNDEBUG:
			print(yellow("Waiting for overlay respose..."))
			time.sleep(0.1)
	globs.got_overlay_response = False
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	return globs.q_response
	x.join()

def overlay_t():
	initial_dict = {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}
	dict_to_send = {"res": []}
	dict_to_send["res"].append(initial_dict)
	return node_overlay(dict_to_send)


@app.route(ends.c_depart ,methods = ['GET'])									# cli (client) operation depart
def cli_depart():
	return cli_depart_func()

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

@app.route(ends.chain_insert ,methods = ['POST'])
def chain_insert():
	data = request.get_json()
	return chain_insert_func(data)

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

def delete_t(pair):
	return delete_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

@app.route(ends.chain_delete ,methods = ['POST'])
def chain_delete():
	data = request.get_json()
	return chain_delete_func(data)

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

@app.route(ends.chain_query ,methods = ['POST'])
def chain_query():
	data = request.get_json()
	return chain_query_func(data)

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
	r_node = request.get_json()
	return node_overlay(r_node)


@app.route(ends.n_insert ,methods = ['POST'])									# chord operation insert(key.value)
def chord_insert():
	print("CHORD N_INSERT HERE")
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

@app.route(ends.b_depart ,methods = ['POST'])									# depart(nodeID)
def boot_depart():
	d_node = request.form.to_dict()
	return boot_depart_func(d_node)

@app.route(ends.b_list ,methods = ['GET'])										# send nodesList
def boot_sendList():
	return boot_send_nodes_list()

def server():
	if len(sys.argv) < 7:
		wrong_input_format()
	if sys.argv[1] in ("-p", "-P"):
		globs.my_port = sys.argv[2]
	else:
		wrong_input_format()
	if sys.argv[3] in ("-k", "-K"):
		globs.k = int(sys.argv[4])
	else:
		wrong_input_format()
	if sys.argv[5] in ("-c", "-C"):
		if sys.argv[6] in ("linear", "l"):
			globs.consistency = "linear"
		elif sys.argv[6] in ("eventual", "e"):
			globs.consistency = "eventual"
		else:
			globs.consistency = "none"
	else:
		wrong_input_format()
	globs.my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	if len(sys.argv) == 8 and sys.argv[7] in ("-b", "-B"):
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
		node_initial_join()

	print("\n\n")
	app.run(host= globs.my_ip, port=globs.my_port,debug = True, use_reloader=False)

def wrong_input_format():
	print(red("Argument passing error!"))
	print(underline("Usage:"))
	print(cyan("-p port_to_open\n -k replication_factor (<= number of nodes)\n -c consistency_type ((linear,l) or (eventual,e))\n -b for bootstrap node only"))
	exit(0)

if __name__ == '__main__':
	server()
