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

app = Flask(__name__)
counter = 0
rcnt = 0


@app.route('/',methods = ['GET'])												# root directory (useless)
def home():
	return "my name is ToyChord"


@app.route(ends.info ,methods = ['GET'])										# cli (client) operation info
def cli_info():
	return globs.my_id + " " + globs.my_ip + " " + globs.my_port


@app.route(ends.c_overlay ,methods = ['GET'])									# cli (client) operation network overlay
def cli_over():
	return client_overlay()

@app.route(ends.c_depart ,methods = ['GET'])										# cli (client) operation depart
def cli_depart():
	return cli_depart_func()

@app.route(ends.c_insert ,methods = ['POST'])										# cli (client) operation insert
def cli_insert():
	pair = request.form.to_dict()
	result = request.post(config.ADDR + globs.my_ip + ":" + globs.my_port + ends.n_insert, data = pair)
	return result

@app.route(ends.c_delete ,methods = ['POST'])										# cli (client) operation delete
def cli_delete():
	pair = request.form.to_dict()
	result = request.post(config.ADDR + globs.my_ip + ":" + globs.my_port + ends.n_delete, data = pair)
	return result

@app.route(ends.c_query ,methods = ['POST'])										# cli (client) operation query
def cli_query():
	pair = request.form.to_dict()
	result = request.post(config.ADDR + globs.my_ip + ":" + globs.my_port + ensd.n_query, data = pair)
	return result

@app.route(ends.n_overlay ,methods = ['POST'])									# chord operation network overlay
def chord_over():
	r_node = request.form.to_dict()
	return node_overlay(r_node)


@app.route(ends.n_insert ,methods = ['POST'])								# chord operation insert(key.value)
def chord_insert():
	if request.method == 'POST':
		result = request.form.to_dict()
		return insert_song(result)

@app.route(ends.n_delete ,methods = ['POST'])									# chord operation delete(key)
def chord_delete():
	if request.method == 'POST':
		result = request.form.to_dict()
		return delete_song(result)

@app.route(ends.n_query ,methods = ['POST'])									# chord operation query(key)
def chord_query():
	if request.method == 'POST':
		result = request.form.to_dict()
		return query_song(result)


@app.route(ends.n_update_peers ,methods = ['POST'])									# update(nodeID)
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
		node_initial_join()

	print("\n\n")
	app.run(host= globs.my_ip, port=globs.my_port,debug = True, use_reloader=False)


if __name__ == '__main__':
	server()
