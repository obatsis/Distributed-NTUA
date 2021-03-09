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
import time


app = Flask(__name__)
counter = 0
rcnt = 0
# address = 'http://localhost:'

# global globs.my_id
# global globs.my_ip
# global globs.my_port

# globs.my_id = 0
# globs.my_ip = 0
# globs.my_port = 0

@app.route('/',methods = ['GET'])												# root directory (useless)
def home():
	return "my name is ToyChord"


@app.route('/cli/info',methods = ['GET'])										# cli (client) operation info
def cli_info():
	return globs.my_id + " " + globs.my_ip + " " + globs.my_port


@app.route('/cli/overlay',methods = ['GET'])									# cli (client) operation network overlay
def cli_over():
	return client_overlay()

@app.route('/cli/depart',methods = ['GET'])										# cli (client) operation depart
def cli_depart():
	pass
@app.route('/cli/insert',methods = ['GET'])										# cli (client) operation insert
def cli_insert():
	pass
@app.route('/cli/delete',methods = ['GET'])										# cli (client) operation delete
def cli_delete():
	pass
@app.route('/cli/query',methods = ['GET'])										# cli (client) operation query
def cli_query():
	pass

@app.route('/chord/overlay',methods = ['POST'])									# chord operation network overlay
def chord_over():
	r_node = request.form.to_dict()
	return node_overlay(r_node)


@app.route('/chord/insert_song',methods = ['POST'])								# chord operation insert(key.value)
def chord_insert():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for insert value {}".format(result["val"]))
		# return "inserted " + result["val"]
		return insert_song(result)

@app.route('/chord/delete_song',methods = ['POST'])									# chord operation delete(key)
def chord_delete():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for delete value {}".format(result["val"]))
		return "deleted " + result["val"]

@app.route('/chord/query_song',methods = ['POST'])									# chord operation query(key)
def chord_query():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for query value {}".format(result["val"]))
		return "queried " + result["val"]


@app.route('/chord/updatePeersList',methods = ['POST'])									# update(nodeID)
def chord_updateList():
	new_neighbours = request.get_json()
	return node_update_list(new_neighbours)


@app.route('/boot/join',methods = ['POST'])										# join(nodeID)
def boot_join():
	if globs.boot:
		new_node = request.form.to_dict()
		return bootstrap_join_func(new_node)
	else:
		print(red("You are not authorized to do this shitt...Therefore you are now DEAD"))
		exit(0)

@app.route('/boot/depart',methods = ['POST'])									# depart(nodeID)
def boot_depart():
	# when a node departs, master has to update everyone with their new neighbours
		pass

# @app.before_first_request
# def initialize():
#     print(blue(" TEST this gets called only once, when the first request comes in"))

def hash(key):
	return hashlib.sha1(key.encode('utf-8')).hexdigest()

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
