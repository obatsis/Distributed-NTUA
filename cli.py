import sys
import requests


address = 'http://localhost:5000/cli'

def main(argv):

	dat = {
		"rid" : "",
		"val": 123
	}

	response = requests.get(address)
	if response.status_code == 200:
		print("ALL GOOD")
	print(response.text)

	response = requests.post('http://localhost:5000/', data = dat)
	if response.status_code == 200:
		print("	ALL GOOD")
	print("response text: {}" .format(response.text))

	response = requests.post(address, data = dat)
	print("response url: {}" .format(response.url))
	print("response status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("	ALL GOOD")
	print("response text: {}" .format(response.text))
	# print("response headers: {}" .format(response.headers))
	print("response elapsed: {}" .format(response.elapsed))
	# print("response content: {}" .format(response.content))
	print("closing connection to server")
	response.close()
	dat["rid"] = "net_overlay"
	response = requests.post(address, data = dat)
	print("response url: {}" .format(response.url))
	print("response status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("	ALL GOOD")
	print("response text: {}" .format(response.text))
	# print("response headers: {}" .format(response.headers))
	print("response elapsed: {}" .format(response.elapsed))
	# print("response content: {}" .format(response.content))
	print("closing connection to server")
	response.close()
	dat["rid"] = "insert"
	response = requests.post(address, data = dat)
	print("response url: {}" .format(response.url))
	print("response status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("	ALL GOOD")
	print("response text: {}" .format(response.text))
	# print("response headers: {}" .format(response.headers))
	print("response elapsed: {}" .format(response.elapsed))
	# print("response content: {}" .format(response.content))
	print("closing connection to server")
	response.close()
	dat["rid"] = "delete"
	response = requests.post(address, data = dat)
	print("response url: {}" .format(response.url))
	print("response status code: {}" .format(response.status_code), end =" ")
	if response.status_code == 200:
		print("	ALL GOOD")
	print("response text: {}" .format(response.text))
	# print("response headers: {}" .format(response.headers))
	print("response elapsed: {}" .format(response.elapsed))
	# print("response content: {}" .format(response.content))
	print("closing connection to server")
	response.close()





if __name__ == "__main__":
   main(sys.argv[1:])
