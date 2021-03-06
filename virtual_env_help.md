# Creating Virtual Environments
The module used to create and manage virtual environments is called venv. venv will usually install the most recent version of Python that you have available. If you have multiple versions of Python on your system, you can select a specific Python version by running python3 or whichever version you want.

## To create a virtual environment, decide upon a directory where you want to place it, and run the venv module as a script with the directory path:

`python3 -m venv distr`

This will create the `distr` directory if it doesn’t exist, and also create directories inside it containing a copy of the Python interpreter, the standard library, and various supporting files.

A common directory location for a virtual environment is .venv. This name keeps the directory typically hidden in your shell and thus out of the way while giving it a name that explains why the directory exists. It also prevents clashing with .env environment variable definition files that some tooling supports.

## Once you’ve created a virtual environment, you may activate it.

On Unix or MacOS, run:

`source distr/bin/activate`
