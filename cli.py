import sys
import requests


address = 'http://localhost:5003/'

def main(argv):

	dat = {
		"rid" : "",
		"val": 123
	}

	# info check test
	response = requests.get(address)


	# net overlay test
	response = requests.get(address + "cli/overlay")
	print("status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("		ALL GOOD")
		print("response: {}" .format(response.text))

	response = requests.get(address + "cli/depart")
	print("status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("		ALL GOOD")
		print("response: {}" .format(response.text))

	# response = requests.post(address + "chord/insert", data = dat)
	# print("status code: {}" .format(response.status_code), end =" ")
	# if response.status_code == 200:
	# 	print("		ALL GOOD")
	# 	print("response: {}" .format(response.text))
	#
	#
	# response = requests.post(address + "chord/delete", data = dat)
	# print("status code: {}" .format(response.status_code), end =" ")
	# if response.status_code == 200:
	# 	print("		ALL GOOD")
	# 	print("response: {}" .format(response.text))
	#
	# response = requests.post(address + "chord/query", data = dat)
	# print("status code: {}" .format(response.status_code), end =" ")
	# if response.status_code == 200:
	# 	print("		ALL GOOD")
	# 	print("response: {}" .format(response.text))
	#
	#
	# response = requests.get(address+"/over")	#intentionally in order to produce an error


	# print(response.url.split("/")[2])
	# print("response url: {}" .format(response.url))
	# print("response text: {}" .format(response.text))
	# print("response headers: {}" .format(response.headers))
	# print("response elapsed: {}" .format(response.elapsed))
	# print("response content: {}" .format(response.content))
	# print("closing connection to server")
	# response.close()



if __name__ == "__main__":
   main(sys.argv[1:])
