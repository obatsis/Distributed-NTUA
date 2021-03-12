import requests
import config
from utils.colorfy import *
import ends
import random
import time

def test_trans(test_number):
	# get the mids list from bootstrap
	nodes = []
	if config.TDEBUG:
		print(cyan("\n Fetching the nodes List from Bootstrap..."))
	try:
		response = requests.get(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + ends.b_list)
		if response.status_code == 200:
			for node in response.text.split(" "):
				nodes.append(node)
			if config.TDEBUG:
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
	if config.TDEBUG:
		print(nodes)


	if test_number == '1':
		# run insert.txt
		infile = open(config.BASE_DIR +"transactions/insert.txt", "r")
		outfile = open(config.BASE_DIR + 'transactions/outputs/insert_results_{}.txt'.format(int(time.time())), "w+")
		for line in infile.readlines():
			line = line.strip()
			parts = line.split(",")
			to_node = random.choice(nodes)
			if config.TDEBUG:
				print(cyan("Inserting song: ") + parts[0] + cyan(" with value: ") + parts[1] + cyan(" to node: ") + to_node)
			try:
				response = requests.post(config.ADDR + to_node + ends.c_insert, data = {'key': parts[0], 'value': parts[1].rstrip("\n")})
				if response.status_code == 200:
					if config.TDEBUG:
						print(response.text)
					outfile.write(response.text + "\n")
				else:
					print("Error while inserting the song...status code: " + red(response.status.code))
			except:
				print(red("\nSomething went wrong!! node doesnt respond"))
	elif test_number == '2':
		# run query.txt
		infile = open(config.BASE_DIR +"transactions/query.txt", "r")
		outfile = open(config.BASE_DIR + 'transactions/outputs/query_results_{}.txt'.format(int(time.time())), "w+")
		for line in infile.readlines():
			line = line.rstrip("\n")	# remove newline from the end of the string
			to_node = random.choice(nodes)
			if config.TDEBUG:
				print(cyan("Query song: ") + line +  cyan(" to node: ") + to_node)
			try:
				response = requests.post(config.ADDR + to_node + ends.c_query, data = {'key': line})
				if response.status_code == 200:
					if config.TDEBUG:
						print(response.text)
					outfile.write(response.text + "\n")
				else:
					print("Error while querying the song...status code: " + red(response.status.code))
			except:
				print(red("\nSomething went wrong!! node doesnt respond"))
	elif test_number == '3':
		# run requests.txt
		infile = open(config.BASE_DIR +"transactions/requests.txt", "r")
		outfile = open(config.BASE_DIR + 'transactions/outputs/requests_results_{}.txt'.format(int(time.time())), "w+")
		for line in infile.readlines():
			line = line.strip()
			parts = line.split(",")
			to_node = random.choice(nodes)
			time.sleep(0.3)
			if parts[0] == "insert":
				if config.TDEBUG:
					print(cyan("Inserting song: ") + parts[1] + cyan(" with value: ") + parts[2].rstrip("\n") + cyan(" to node: ") + to_node)
				try:
					response = requests.post(config.ADDR + to_node + ends.c_insert, data = {'key': parts[1], 'value': parts[2].rstrip("\n")})
					if response.status_code == 200:
						if config.TDEBUG:
							print(response.text)
						outfile.write(response.text + "\n")
					else:
						print("Error while inserting the song...status code: " + red(response.status.code))
				except:
					print(red("\nSomething went wrong!! node doesnt respond"))

			elif parts[0] == "query":
				if config.TDEBUG:
					print(cyan("Query song: ") + parts[1].rstrip("\n") +  cyan(" to node: ") + to_node)
				try:
					response = requests.post(config.ADDR + to_node + ends.c_query, data = {'key': parts[1].rstrip("\n")})
					if response.status_code == 200:
						if config.TDEBUG:
							print(response.text)
						outfile.write(response.text + "\n")
					else:
						print("Error while querying the song...status code: " + red(response.status.code))
				except:
					print(red("\nSomething went wrong!! node doesnt respond"))

	infile.close()
	outfile.close()
