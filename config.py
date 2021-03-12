import os
cwd = os.getcwd()    # Returns 'abcdc'  # Get the current working directory (cwd)
BASE_DIR = cwd[:-4]

NETIFACE = "lo"	# this shoulb be eth0 or em0 in order for the vms to work
BOOTSTRAP_IP = "127.0.0.1"	# fix this
BOOTSTRAP_PORT = "5000"
ADDR = 'http://'
BDEBUG = True		# debug information for bootstrap operations
NDEBUG = True		# debug information for node operations
TDEBUG = False		# debug information fot test operations
vBDEBUG = False		# extra verbose debug information for bootstrap operations
vNDEBUG = False		# extra verbose debug information for node operations
k = 1
