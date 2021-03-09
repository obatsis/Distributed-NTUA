import requests
import os
from PyInquirer import style_from_dict, Token, prompt
import sys
import ends
import config
from utils.colorfy import *
style = style_from_dict({
	Token.QuestionMark: '#E91E63 bold',
	Token.Selected: '#673AB7 bold',
	Token.Instruction: '#0bf416',
	Token.Answer: '#2196f3 bold',
	Token.Question: '#0bf416 bold',
})

def client(ip, port):
	os.system('cls||clear')
	yellow('What a beautiful day to enter the cult...')
	baseURL = 'http://' + ip + ':' + port

	while True:
		print('----------------------------------------------------------------------')
		method_q = {
			'type': 'list',
			'name': 'method',
			'message': 'Select action:',
			'choices': ['Network Overlay', \
						'Insert a Song', \
						'Search for a Song', \
						'Delete a Song', \
						'Depart from Chord', \
						'Help', \
						'Exit']
		}
		method_a = prompt(method_q, style=style)['method']

		if method_a == 'Depart from Chord':
			print(yellow("Preparing Node to depart from Chord..."))
			try:
				response = requests.get(baseURL + ends.c_depart)
				if response.status_code == 200:
					if response.text == "Left the Chord":
						print(response.text)
						print(green("Node is out of Toychord network"))
					else:
						print(red(response.text))
				else :
					print(red("Got a bad response status code " + response.status_code))
			except:
				print(red("Could not establish connection with Node. Node didnt depart..."))
				print(red("Unfortunately exiting..."))
			break

		elif method_a == 'Insert a Song':
			print('Insert a Title-Value pair for the song you wish to insert')
			fetch_q = [
			{
				'type': 'input',
				'name': 'key',
				'message': 'Song Title:',
				'filter': lambda val: str(val)
			},
			{
				'type': 'input',
				'name': 'value',
				'message': 'Value:',
				'filter': lambda val: str(val)
			}
			]
			fetch_a = prompt(fetch_q, style=style)
			print(yellow("Inserting Song: ") + fetch_a['key'] + yellow(" ..."))
			try:
				response = requests.post(baseURL + ends.c_insert ,data={'key':fetch_a['key'],'value':fetch_a['value']})
				if response.status_code == 200:
					print("Inserted by node with id ",green(response.text))
				else :
					print(red("Got a bad response status code " + response.status_code))
			except:
				print(red("Could not establish connection with Node. Song wasnt inserted..."))
				print(red("Unfortunately exiting..."))
				exit(0)

			continue

		elif method_a == 'Delete a Song':
			print('Insert the Song Title you wish to delete')
			fetch_q = [
			{
				'type': 'input',
				'name': 'key',
				'message': 'Song Title:',
				'filter': lambda val: str(val)
			}]
			fetch_a = prompt(fetch_q, style=style)
			print(yellow("Deleting Song: ") + fetch_a['key'] + yellow(" ..."))
			try:
				response = requests.post(baseURL + ends.c_delete ,data={'key':fetch_a['key']})
				if response.status_code == 200:
					print(green(response.text))
				else :
					print(red("Got a bad response status code " + response.status_code))
			except:
				print(red("Could not establish connection with Node. Song wasnt deleted..."))
				print(red("Unfortunately exiting..."))
				exit(0)

			continue

		elif method_a == 'Search for a Song':
			print('Insert the Song Title you wish to Search')
			fetch_q = [
			{
				'type': 'input',
				'name': 'key',
				'message': 'Song Title:',
				'filter': lambda val: str(val)
			}]
			fetch_a = prompt(fetch_q, style=style)
			print(yellow("Searching Song: ") + fetch_a['key'] + yellow(" ..."))
			try:
				response = requests.post(baseURL + ends.c_query ,data={'key':fetch_a['key']})
				if response.status_code == 200:
					if response.text in ("None","null"):
						print("Song not found")
					else:
						print("Song found in node with id ",green(response.text))
				else:
					print(red("Got a bad response status code " + response.status_code))
			except:
				print(red("Could not establish connection with Node. Couldnt search for song..."))
				print(red("Unfortunately exiting..."))
				exit(0)

			continue

		elif method_a == 'Network Overlay':
			print(yellow("Initiating Network Overlay..."))
			try:
				response = requests.get(baseURL + ends.c_overlay)
				if response.status_code == 200:
					print(green(response.text))
				else :
					print(red("Got a bad response status code " + response.status_code))
			except:
				print(red("Could not establish connection with Node..."))
				print(red("Unfortunately exiting..."))
				exit(0)

			continue

		elif method_a == 'Help':
			print('-------------------------------- Help --------------------------------\n')

			overlayHelp="Overlay: This functions recreates and prints the current Network Topology(eg. Node1 -> Node2 -> ...)"
			insertHelp="Insert Song: This functions expects a Song Title and a Song Value and inserts them in the Chord (eg. )"
			queryHelp="Search Song: This function expects a Song Title and searches the Node in whitch the song is stored"
			deleteHelp="deleteHelp"
			departHelp="departHelp"

			print(	" -",overlayHelp,"\n"
					" -",insertHelp,"\n",
					"-",queryHelp,"\n",
					"-",deleteHelp,"\n",
					"-",departHelp,"\n",
					)

			continue

		elif method_a == 'Exit':
			os.system('cls||clear')

			break

		else:
			continue

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
	if sys.argv[1] in ("-p", "-P"):
		my_port = sys.argv[2]
		my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
		client(my_ip, my_port)
