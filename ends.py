global info		# GET: returns info about the node
info = '/cli/info'

global c_overlay # GET: starts overlay from this node and returns the topology
c_overlay = '/cli/overlay'

global c_depart # GET: starts the depart procedure of the node and returns the status
c_depart = '/cli/depart'

global c_insert	# POST: inserts a song {song key, val}
c_insert = '/cli/insert'

global c_delete 	# POST: deletes a song {song key}
c_delete = '/cli/delete'

global c_query	# POST: returns info about the song	{song key}
c_query = '/cli/query'

global n_overlay # POST: returns node info plus previous overlay info {node id, ip, port}
n_overlay = '/chord/overlay'

global n_insert	# POST: inserts a song {song key, val}
n_insert = '/chord/insert'

global n_delete # POST: deletes a song {song key}
n_delete = '/chord/delete'

global n_query 	# POST: returns info about the song	{song key}
n_query = '/chord/query'

global n_update_peers 	# POST: update node peers list {prev {node id, ip, port}, next {node id, ip, port}}
n_update_peers = '/chord/updatePeersList'

global b_join	# POST: adds node to the Chord {node id, ip, port}
b_join = '/boot/join'

global b_depart # POST: removes node from the Chord {node id, ip, port}
b_depart = '/boot/depart'

global b_list # GET: returns the list of all nodes (ip:port ip:port ....)
b_list = '/boot/listNodes'
