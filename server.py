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


@app.route('/',methods = ['GET'])												# root directory (basically system info and οτι αλλο προκυψει)
def home():
	global counter
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
	if boot:
		new_node = request.form.to_dict()
		candidate_id = new_node["uid"]
		print(yellow(candidate_id) + "  wants to join the Chord with ip:port " + yellow(new_node["ip"] + ":" + new_node["port"]))
		for idx, ids in enumerate(mids):
			if candidate_id < ids["uid"]:
				mids.insert(idx, new_node)
				break
			elif idx == len(mids)-1:
				mids.append(new_node)
				break
		print(mids)
		new_node_idx = mids.index(new_node)
		print("new node possition in mids: " + str(new_node_idx))
		# we must return strings probably....i dont know...
		# and we have to find the bug bellow
		# return mids[new_node_idx-1] if new_node_idx >= 1 else mids[-1] + " " + mids[new_node_idx+1] if new_node_idx < len(mids)-1 else mids[0]
		return "ok"

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
		my_port = sys.argv[2]
	my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	if len(sys.argv) == 4 and sys.argv[3] in ("-b", "-B"):
		print("I am the Bootstrap Node with ip: " + yellow(my_ip) + " about to run a Flask server on port "+ yellow(my_port))
		my_id = hash(my_ip + my_port)
		print("and my unique id is: " + green(my_id))
		boot = True
		# mids["uid"] = my_id	#boot is the first one to enter the list
		# mids["ip"] = my_ip	#boot is the first one to enter the list
		# mids["port"] = my_port	#boot is the first one to enter the list
		mids.append({"uid":my_id, "ip":my_ip, "port":my_port})	#boot is the first one to enter the list
	else:
		boot = False
		print("I am a normal Node with ip: " + yellow(my_ip) + " about to run a Flask server on port "+ yellow(my_port))
		my_id = hash(my_ip + my_port)
		print("and my unique id is: " + green(my_id))
		print(yellow("\natempting to join the Chord..."))
		try:
			response = requests.post(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + "/boot/join", data = {"uid" : my_id, "ip": my_ip, "port" : my_port})
			if response.status_code == 200:
				print(response.text)
			else:
				print("Something went wrong!!  status code: " + red(response.status.code))
				print(red("\nexiting..."))
				exit(0)
		except:
			print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
			print(red("\nexiting..."))
			exit(0)

	print("\n\n")
	app.run(host= my_ip, port=my_port,debug = True, use_reloader=False)
