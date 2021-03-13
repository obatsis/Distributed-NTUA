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

@app.route(ends.c_depart ,methods = ['GET'])										# cli (client) operation depart
def cli_depart():
	return cli_depart_func()

@app.route(ends.c_insert ,methods = ['POST'])										# cli (client) operation insert
def cli_insert():
	pair = request.form.to_dict()
	globs.started_insert = True
	x = threading.Thread(target=insert_t ,args = [pair])
	x.start()
	while not(globs.got_insert_response):
		if config.NDEBUG:
			print(yellow("Waiting for insert respose..."))
		time.sleep(0.5)
	globs.got_insert_response = True
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	time.sleep(0.1)
	return globs.q_responder + " " + globs.q_response
	x.join()

def insert_t(pair):
	return insert_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

@app.route(ends.c_delete ,methods = ['POST'])										# cli (client) operation delete
def cli_delete():
	pair = request.form.to_dict()
	globs.started_delete = True
	x = threading.Thread(target=delete_t ,args = [pair])
	x.start()
	while not(globs.got_delete_response):
		if config.NDEBUG:
			print(yellow("Waiting for delete respose..."))
		time.sleep(0.5)
	globs.got_delete_response = True
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	time.sleep(0.1)
	return globs.q_responder + " " + globs.q_response
	x.join()

def delete_t(pair):
	return delete_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})


@app.route(ends.c_query ,methods = ['POST'])										# cli (client) operation query
def cli_query():
	pair = request.form.to_dict()
	globs.started_query = True
	x = threading.Thread(target=query_t ,args = [pair])
	x.start()
	while not(globs.got_query_response):
		if config.NDEBUG:
			print(yellow("Waiting for query respose..."))
		time.sleep(0.5)
	globs.got_query_response = True
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	time.sleep(0.1)
	return globs.q_responder + " " + globs.q_response
	x.join()

def query_t(pair):
	return query_song({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

@app.route(ends.c_query_star ,methods = ['POST'])								# cli (client) operation query *
def cli_query_star():
	globs.started_query_star = True
	x = threading.Thread(target=query_star_t ,args = [])
	x.start()
	while not(globs.got_query_star_response):
		if config.NDEBUG:
			print(yellow("Waiting for query_star respose..."))
		time.sleep(0.5)
	globs.got_query_star_response = True
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	# time.sleep(0.1)
	# return globs.q_responder + " " + globs.q_response
	return
	x.join()

def query_star_t(pair):
	return query_star_song()


@app.route(ends.n_overlay ,methods = ['POST'])									# chord operation network overlay
def chord_over():
	r_node = request.form.to_dict()
	return node_overlay(r_node)


@app.route(ends.n_insert ,methods = ['POST'])								# chord operation insert(key.value)
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

@app.route(ends.b_list ,methods = ['GET'])									# send nodesList
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
		node_initial_join()

	print("\n\n")
	app.run(host= globs.my_ip, port=globs.my_port,debug = True, use_reloader=False)


if __name__ == '__main__':
	server()
