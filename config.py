import os
import globs

cwd = os.getcwd()	# Get the current working directory (cwd)
BASE_DIR = cwd[:-4]	# remove auto/

NETIFACE = "lo"	# this shoulb be eth0 or em0 in order for the vms to work
BOOTSTRAP_IP = "127.0.0.1"	# fix this
BOOTSTRAP_PORT = "5000"
ADDR = 'http://'
BDEBUG = True		# debug information for bootstrap operations
NDEBUG = True		# debug information for node operations
TDEBUG = False		# debug information fot test operations
vBDEBUG = False		# extra verbose debug information for bootstrap operations
vNDEBUG = False		# extra verbose debug information for node operations

KAPPA = globs.k
CONSISTENCY = globs.consistency
