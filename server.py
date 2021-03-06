import sys
from flask import Flask, request
import requests
app = Flask(__name__)
messages={}
counter = 0
rcnt = 0
address = 'http://localhost:'

@app.route('/',methods = ['POST', 'GET'])
def home():
	global counter
	if request.method == 'GET':
		counter += 1
		print("-- Just got a GET request and local cnt is: {}".format(counter))
		return "my name is orestis " + str(counter)

	if request.method == 'POST':
		result = request.form.to_dict()

		print(result["id"])
		print(result["val"])

		return str(int(result["val"])+1)

@app.route('/cli',methods = ['POST', 'GET'])
def katiti():
	global rcnt
	rcnt += 1
	if request.method == 'GET':
		print("-- Just got a GET request and local cnt is: {}".format(rcnt))
		return "my name is orestis " + str(rcnt)

	if request.method == 'POST':
		result = request.form.to_dict()

		if result["rid"] == "net_overlay":
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
		elif result["rid"] == "insert":
			print("got request for insert value {}".format(result["val"]))
		elif result["rid"] == "delete":
			print("got request for delete value {}".format(result["val"]))
		else:
			print("Uknown request")
			return "Bad Request"

		return str(rcnt)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
	if sys.argv[1] in ("-p", "-P"):
		op_port = sys.argv[2]
	if len(sys.argv) == 4 and sys.argv[3] in ("-b", "-B"):
		print("	-- Special Node (Bootstrap)")

	app.run(port=op_port,debug = True)
