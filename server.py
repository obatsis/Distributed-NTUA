import os
import sys
import hashlib
from flask import Flask, request
import requests
from  api import *
import config
from utils.colorfy import *
app = Flask(__name__)
messages={}
counter = 0
rcnt = 0
address = 'http://localhost:'

# here we must have a list or something to save the next and prev Node
# we must save both ip and port in order to be compatible with the vms when the time comes
global boot, my_ip, my_id, nids, mids
mids = []
nids = []
@app.route('/',methods = ['GET'])												# root directory (basically system info and οτι αλλο προκυψει)
def home():
	global counter
	# global boot, my_ip, my_id, nids, mids
	if request.method == 'GET':
		counter += 1
		print("-- Just got a GET request and local cnt is: {}".format(counter))
		return "my name is ToyChord and a have a counter: " + str(counter)

# xreiazontai 2 endpoints gia joint dioti o 1os komvos tha einai blocked apo to
#join tou cli...opote oi  komvoi metaksi tous tha prepei na milane me allo endpoint gia to overlay
@app.route('/cli/overlay',methods = ['GET'])							# cli (client) operation network overlay
def cli_over():
	print("got request for net overlay")
	# if request.host == "localhost:5000":
	if int(request.host.split(":")[1]) < 5002:
		try:
			response = requests.post(address + str(int(request.host.split(":")[1]) + 1) + "/cli", data = {"rid": "net_overlay", "val": "none"})
			if response.status_code == 200:
				return request.host + " -> " + response.text
		except:
		  print("the other one is dead")
		  return request.host + " -> the other one is dead"
	else:
		return request.host

@app.route('/cli/depart',methods = ['GET'])										# cli (client) operation depart
def cli_depart():
	pass

@app.route('/chord/overlay',methods = ['GET'])									# chord operation network overlay
def chord_over():
	pass


@app.route('/chord/insert',methods = ['POST'])									# chord operation insert(key.value)
def chord_insert():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for insert value {}".format(result["val"]))
		# return "inserted " + result["val"]
		return insert_song(result)

@app.route('/chord/delete',methods = ['POST'])									# chord operation delete(key)
def chord_delete():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for delete value {}".format(result["val"]))
		return "deleted " + result["val"]

@app.route('/chord/query',methods = ['POST'])									# chord operation query(key)
def chord_query():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for query value {}".format(result["val"]))
		return "queried " + result["val"]

# when a node departs, master has to update everyone with their new neighbours
@app.route('/node/update',methods = ['POST'])									# update(nodeID)
def node_update():
	pass

@app.route('/boot/join',methods = ['POST'])										# join(nodeID)
def boot_join():
	result = request.form.to_dict()
	candidate_id
	print(yellow(result["uid"]) + "  wants to join the Chord")
	for ids in mids:
		pass
	return "OK BRO"


@app.route('/boot/depart',methods = ['POST'])									# depart(nodeID)
def boot_depart():
	if request.method == 'POST':
		pass

@app.before_first_request
def initialize():
    print(blue(" TEST this gets called only once, when the first request comes in"))

def hash(key):
	return hashlib.sha1(key.encode('utf-8')).hexdigest()

if __name__ == '__main__':
	print("\n")
	if len(sys.argv) < 3:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
	if sys.argv[1] in ("-p", "-P"):
		op_port = sys.argv[2]
	my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	if len(sys.argv) == 4 and sys.argv[3] in ("-b", "-B"):
		print("I am the Bootstrap Node with ip: " + yellow(my_ip) + " about to run a Flask server on port "+ yellow(op_port))
		print("and my unique id is: " + green(hash(my_ip + op_port)))
		boot = True
		mids.append(my_id)	#boot is the first one to enter the list
	else:
		boot = False
		print("I am a normal Node with ip: " + yellow(my_ip) + " about to run a Flask server on port "+ yellow(op_port))
		my_id = hash(my_ip + op_port)
		print("and my unique id is: " + green(my_id))
		print(yellow("\natempting to join the Chord..."))
		try:
			response = requests.post(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + "/boot/join", data = {"uid" : my_id})
			if response.status_code == 200:
				print(response.text)

		except:
			print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
			print(red("\nexiting..."))
			exit(0)

	print("\n\n")
	app.run(host= my_ip, port=op_port,debug = True, use_reloader=False)
