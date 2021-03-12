import requests
import config
from utils.colorfy import *


def test_trans(test_number, method):
	# get the mids list from bootstrap
	print(yellow("\n Fetching the nodes List from Bootstrap"))
	try:
		response = requests.get(config.ADDR + config.BOOTSTRAP_IP + ":" + config.BOOTSTRAP_PORT + ends.b_list)
		if response.status_code == 200:
			for node in response.text.split(" "):
				nodes.append(node)

			print(yellow("Got the nodes successfully"))
		else:
			print("Something went wrong while fetching the nodes from bootstrap  status code: " + red(response.status.code))
			print(red("\nexiting..."))
			exit(0)
	except:
		print(red("\nSomething went wrong!! (check if bootstrap is up and running)"))
		print(red("\nexiting..."))
		exit(0)

	print(nodes)
	if test_number == '1':
		# run insert.txt
		pass
	elif test_number == '2':
		# run query.txt
		pass
	elif test_number == '3':
		# run requests.txt
		pass
