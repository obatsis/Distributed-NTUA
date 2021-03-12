import requests
import config
from utils.colorfy import *
import ends
import random
import os

def test_trans(test_number):
	# get the mids list from bootstrap
	nodes = []
	print(cyan("\n Fetching the nodes List from Bootstrap..."))
	try:
		response = requests.get(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + ends.b_list)
		if response.status_code == 200:
			for node in response.text.split(" "):
				nodes.append(node)
			print(cyan("Got the nodes successfully"))
		else:
			print(red("Something went wrong while fetching the nodes from bootstrap  status code: ") + response.status.code)
			print(red("\nexiting..."))
			exit(0)
	except:
		print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
		print(red("\nexiting..."))
		exit(0)
	nodes.remove('') # remove the last element which is ''
	print(nodes)


	if test_number == '1':
		# run insert.txt

		cwd = os.getcwd()  # Get the current working directory (cwd)
		files = os.listdir(cwd)  # Get all the files in that directory
		print("Files in %r: %s" % (cwd, files))
		
		f = open("/insert.txt", "r")
		for line in f.readlines():
			line = line.strip()
			parts = line.split(",")
			to_node = random.choice(nodes)

			print(cyan("Inserting song: ") + parts[0] + cyan(" with value: ") + parts[1] + cyan(" to node: ") + to_node)
			try:
				response = requests.post(config.ADDR + to_node + ends.c_insert, data = {"key": parts[0], "value": parts[1]})
				if response.status_code == 200:
					print(respose.text)
				else:
					print("Error while inserting the song...status code: " + red(response.status.code))
			except:
				print(red("\nSomething went wrong!! node doesnt respond"))
		f.close()
	elif test_number == '2':
		# run query.txt
		pass
	elif test_number == '3':
		# run requests.txt
		pass
