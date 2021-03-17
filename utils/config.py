import os
import utils.globs as globs
# master public ip: 83.212.74.75

cwd = os.getcwd()	# Get the current working directory (cwd)

machine_name = os.uname().nodename
if  machine_name == "master":
	NETIFACE = "eth2"	# master is connected to LAN via eth2 interface and to the world via eth1
	BOOTSTRAP_IP = "192.168.0.2"	# fix this
	BASE_DIR = cwd
elif machine_name.startswith('node'):
	NETIFACE = "eth1"	# vms are connected to LAN via eth1 interface
	BOOTSTRAP_IP = "192.168.0.2"	# fix this
	BASE_DIR = cwd
else:
	NETIFACE = "lo"		# for local execution
	BOOTSTRAP_IP = "127.0.0.1"	# fix this
	BASE_DIR = cwd[:-4]	# remove auto/

BOOTSTRAP_PORT = "5000"
ADDR = 'http://'
BDEBUG = True		# debug information for bootstrap operations
NDEBUG = True		# debug information for node operations
TDEBUG = False		# debug information fot test operations
vBDEBUG = False		# extra verbose debug information for bootstrap operations
vNDEBUG = False		# extra verbose debug information for node operations

KAPPA = globs.k
CONSISTENCY = globs.consistency
