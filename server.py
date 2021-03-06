import sys
from flask import Flask, request
import werkzeug
import requests
app = Flask(__name__)
messages={}
counter = 0
rcnt = 0
address = 'http://localhost:'

# here we must have a list or something to save the next and prev Node
# we must save both ip and port in order to be compatible with the vms when the time comes


@app.route('/',methods = ['GET'])												# root directory (basically system info and οτι αλλο προκυψει)
def home():
	global counter
	global boot
	if request.method == 'GET':
		counter += 1
		print("-- Just got a GET request and local cnt is: {}".format(counter))
		return "my name is ToyChord and a have a counter: " + str(counter)


@app.route('/cli/overlay',methods = ['GET'])							# cli (client) operations network overlay
def cli():
	if request.method == 'GET':
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

@app.route('/chord/insert',methods = ['POST'])									# chord operation insert(key.value)
def chord_insert():
	if request.method == 'POST':
		result = request.form.to_dict()
		print("got request for insert value {}".format(result["val"]))
		return "inserted " + result["val"]

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

@app.route('/boot/join',methods = ['POST'])										# join(nodeID)
def boot_join():
	if request.method == 'POST':
		pass

@app.route('/boot/depart',methods = ['POST'])									# depart(nodeID)
def boot_depart():
	if request.method == 'POST':
		pass

# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'Very bad request!', 400

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
	if sys.argv[1] in ("-p", "-P"):
		op_port = sys.argv[2]
	if len(sys.argv) == 4 and sys.argv[3] in ("-b", "-B"):
		print("	-- Special Node (Bootstrap)")
		boot = True
	else: boot = False
	app.run(port=op_port,debug = True)
