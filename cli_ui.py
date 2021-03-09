import requests
import os
from PyInquirer import style_from_dict, Token, prompt
import sys
import ends
import config

style = style_from_dict({
	Token.QuestionMark: '#E91E63 bold',
	Token.Selected: '#673AB7 bold',
	Token.Instruction: '#0bf416',
	Token.Answer: '#2196f3 bold',
	Token.Question: '#0bf416 bold',
})

def red(string):
	return '\033[1;91m {}\033[00m\n'.format(string)

def yellow(string):
	return '\033[1;93m {}\033[00m\n'.format(string)

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
			'choices': ['Depart', \
						'Insert', \
						'Delete', \
						'Query', \
						'Overlay', \
						'Help', \
						'Exit']
		}
		method_a = prompt(method_q, style=style)['method']

		if method_a == 'Depart':
			print("Node departure...")
			departURL = ends.c_depart
			endpoint = baseURL + departURL
			response = requests.get(endpoint)
			if response.text == "Left the Chord":
				print(response.text)
				print("Node is out of Toychord network")
				exit(0)
			else:
				print(response.text)

			continue

		elif method_a == 'Insert':
			print('Insert key-value pair...')
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
			print(fetch_a['key'])
			print(fetch_a['value'])
			insertURL = ends.c_insert
			endpoint = baseURL + insertURL
			print(endpoint)
			response = requests.post(endpoint,data={'key':fetch_a['key'],'value':fetch_a['value']})

			print(response.text)

			continue

		elif method_a == 'Delete':
			print('Delete key...')

			deleteURL = ends.c_delete
			endpoint = baseURL + deleteURL
			# response = requests.post(endpoint)


			continue

		elif method_a == 'Query':
			print('Query key...')

			queryURL = ends.c_query
			endpoint = baseURL + queryURL
			# response = requests.post(endpoint)
			continue


		elif method_a == 'Overlay':
			print('Overlay key...')

			overlayURL = ends.c_overlay
			endpoint = baseURL + overlayURL
			response = requests.get(endpoint)
			print("OVERLAY OPERATION: ",response.text)

			continue

		elif method_a == 'Help':
			print('---- Help ----\n')

			joinHelp="joinHelp"
			departHelp="departHelp"
			insertHelp="insertHelp"
			deleteHelp="deleteHelp"
			queryHelp="queryHelp"
			overlayHelp="overlayHelp"

			print(" -",joinHelp,"\n",\
				"-",departHelp,"\n",\
				"-",insertHelp,"\n",\
				"-",deleteHelp,"\n",\
				"-",queryHelp,"\n",\
				"-",overlayHelp,"\n"
				)

			continue

		elif method_a == 'Exit':
			os.system('cls||clear')

			break

		else:
			break

if __name__ == '__main__':
	if sys.argv[1] in ("-p", "-P"):
		my_port = sys.argv[2]
		my_ip = os.popen('ip addr show ' + config.NETIFACE + ' | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
		client(my_ip, my_port)
	else:
		print("!! you must tell me the port. Ex. -p 5000 !!")
		exit(0)
