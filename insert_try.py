@app.route(ends.c_insert ,methods = ['POST'])										# cli (client) operation query
def cli_query():
	pair = request.form.to_dict()
	globs.started_insert = True
	x = threading.Thread(target=insert_t ,args = [pair])
	x.start()
	while not(globs.got_insert_response):
		if config.NDEBUG:
			print(yellow("Waiting for query respose..."))
		time.sleep(0.5)
	globs.got_insert_response = True
	if config.NDEBUG:
		print(yellow("Got response, returning value to cli"))
	time.sleep(0.2)
	return globs.in_responder + " " + globs.in_response
	x.join()

def insert_t(pair):
	return insert_song_v2({"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": pair})

#------------------------------------------------------------------------------------------------------------------------------------------#

def eventual_insert(ploads):
    data = ploads
    globs.got_insert_eventual_response = True
    r = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.eventual_insert, json = data)
    return r.text


@app.route(ends.eventual_insert, methods = ['POST'])
def chain_insert():
    data = request.get_json()
    song_for_chain = data[song]
    k = data[chain_length]["k"]
    next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
    song_to_be_inserted = found(song_for_chain["key"])
    if(song_to_be_inserted):
        globs.songs.remove(song_to_be_inserted)
        if config.NDEBUG:
            print(yellow('Updating song: {}').format(song_to_be_inserted))
            print(yellow("To song: 	{}").format(song_for_chain))
            if config.vNDEBUG:
                print(yellow("My songs are now:"))
                print(globs.songs)
    globs.songs.append({"key":song_for_chain["key"], "value":song_for_chain["value"]}) # inserts the (updated) pair of (key,value)
    if config.NDEBUG:
        print(yellow('Inserted song: {}').format(song_for_chain))
        if config.vNDEBUG:
            print(yellow("My songs are now:"))
            print(globs.songs)
    if(k!=1):
        r = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.eventual_insert, json = {data[who], "song":{"key":song_for_chain["key"], "value":song_for_chain["value"]}, "chain_length":{"k":k-1})
        return r.text
    else:
        return song_for_chain

def insert_song(args):
	song = args["song"]
	who_is = args["who"]
	if who_is["uid"] != globs.my_id and globs.started_insert:
		# i am the node who requested the insertion of the song and i am here because the node who has the song sent it to me
		if config.NDEBUG:
			print(yellow("Got response directly from the source: ") + who_is["uid"])
			print(yellow("and it contains: ") + str(song))
			print(yellow("sending confirmation to source node"))
		globs.q_responder = who_is["uid"]
		globs.q_response = song["key"]
		globs.started_insert = False
		globs.got_insert_response = True
		return globs.my_id + " " + song["key"]

	hashed_key = hash(song["key"])
	if config.NDEBUG:
		print(yellow("Got request to insert song: {}").format(song))
		print(yellow("From node: ") + who_is["uid"])
		print(yellow("Song Hash: ") + hashed_key)
	previous_ID = globs.nids[0]["uid"]
	next_ID = globs.nids[1]["uid"]
	self_ID = globs.my_id
	who = 1
	if previous_ID > self_ID and next_ID > self_ID:
		who = 0	# i have the samallest id
	elif previous_ID < self_ID and next_ID < self_ID:
		who = 2 # i have the largest id

	if(hashed_key > previous_ID and hashed_key <= self_ID and who != 0) or (hashed_key > previous_ID and hashed_key > self_ID and who == 0) or (hashed_key <= self_ID and who == 0):
		# song goes in me
		song_to_be_inserted = found(song["key"])
		if(song_to_be_inserted):
			globs.songs.remove(song_to_be_inserted)
			if config.NDEBUG:
				print(yellow('Updating song: {}').format(song_to_be_inserted))
				print(yellow("To song: 	{}").format(song))
				if config.vNDEBUG:
					print(yellow("My songs are now:"))
					print(globs.songs)
		globs.songs.append({"key":song["key"], "value":song["value"]}) # inserts the (updated) pair of (key,value)
		if config.NDEBUG:
			print(yellow('Inserted song: {}').format(song))
			if config.vNDEBUG:
				print(yellow("My songs are now:"))
				print(globs.songs)

        if (globs.consistency == "eventual" and globs.k != 1): # k, consistency πως θα τα εισαγουμε
                ploads = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port},"song":{"key":args["key"], "value":args["value"]}, "chain_length":{"k":k-1}}
                t = Thread(target=eventual_insert, args=[ploads])
                t.start()
                while not(globs.got_insert_eventual_response): # insert a global -> glos.got_insert_eventual_response
                    if config.NDEBUG:
            			print(yellow("Waiting for insert_eventual respose..."))
            		time.sleep(0.5)
                globs.got_insert_eventual_response = True
                time.sleep(0.2)

                if globs.started_insert:# it means i requested the insertion of the song, and i am responsible for it
        			globs.q_response = song["key"]
        			globs.q_responder = who_is["uid"]
        			globs.started_insert = False
        			globs.got_insert_response = True
        			if config.NDEBUG:
        				print(cyan("Special case ") + "it was me who made the request and i also have the song")
        				print(yellow("Returning to myself..."))
        			return "sent it to myself"
        		try: # send the key of the song to the node who requested the insertion
        			result = requests.post(config.ADDR + who_is["ip"] + ":" + who_is["port"] + ends.n_insert, json = {"who": {"uid" : globs.my_id, "ip": globs.my_ip, "port" : globs.my_port}, "song": song})
        			if result.status_code == 200 and result.text.split(" ")[0] == who_is["uid"]:
        				if config.NDEBUG:
        					print("Got response from the node who requested the insertion of the song: " + yellow(result.text))
        				return self_ID + song["key"]
        			else:
        				print(red("node who requested the insertion of the song respond incorrectly, or something went wrong with the satus code (if it is 200 in prev/next node, he probably responded incorrectly)"))
        				return "Bad status code: " + result.status_code
        		except:
        			print(red("node who requested the insertion of the song dindnt respond at all"))
        			return "Exception raised node who requested the insertion of the song dindnt respond"

                t.join()

	elif((hashed_key > self_ID and who != 0) or (hashed_key > self_ID and hashed_key < previous_ID and who == 0) or (hashed_key <= next_ID and who !=0) or (hashed_key <= previous_ID and hashed_key > next_ID and who == 2)):
		# forward song to next
		if config.NDEBUG:
			print(yellow('forwarding to next..'))
		try:
			result = requests.post(config.ADDR + globs.nids[1]["ip"] + ":" + globs.nids[1]["port"] + ends.n_insert, json = {"who": who_is, "song": song})
			if result.status_code == 200:
				if config.NDEBUG:
					print("Got response from next: " + yellow(result.text))
				return result.text
			else:
				print(red("Something went wrong while trying to forward insert to next"))
				return "Bad status code: " + result.status_code
		except:
			print(red("Next is not responding to my call..."))
			return "Exception raised while forwarding to next"
		return self_ID
	else :
		print(red("The key hash didnt match any node...consider thinking again about your skills"))
		return "Bad skills"
