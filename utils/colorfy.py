
## Uppercase is BOLT
# to use: from utils.beautyfy import *
def red(string):
    return '\033[1;91m {}\033[00m'.format(string)

def RED(string):
    return '\033[1;91m {}\033[00m'.format(string)

def yellow(string):
    return '\033[93m {}\033[00m'.format(string)

def YELLOW(string):
    return '\033[1;93m {}\033[00m'.format(string)

def blue(string):
    return '\033[94m {}\033[00m'.format(string)

def BLUE(string):
    return '\033[1;94m {}\033[00m'.format(string)

def green(string):
    return '\033[92m {}\033[00m'.format(string)

def GREEN(string):
    return '\033[1;92m {}\033[00m'.format(string)
	
    # HEADER = '\033[95m'
    # OKBLUE = '\033[94m'
    # OKCYAN = '\033[96m'
    # OKGREEN = '\033[92m'
    # WARNING = '\033[93m'
    # FAIL = '\033[91m'
    # ENDC = '\033[0m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'
