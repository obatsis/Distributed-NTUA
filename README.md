# Distributed-NTUA
`Distributed Systems Course 2020-2021`
ToyChord file shearing Distributed Project


## Before you start navigate to `/help`
1. Read `virtual_env_help.md` and after creating your virtual environment,
activate it by running `source distr/bin/activate`
2. Then run `.scripts/dependencies.sh` with root privileges to install all dependencies.
3. Inside your virtual environment navigate to `/auto` and run `./run_local.sh 10 1 l`
in order to setup 10 nodes with replication factor 1 and linear consistency
in the chord (local execution).

## When you are ready to move your application to okeanos
1. Follow the instructions in `/help``okeanos_scripts_help.md`
2. Now you are ready to sart the ToyChord. Navigate to `/Distributed-NTUA/auto`
and run the script 'run_vms.sh 1 l' from master. This should setup 10 nodes with
replication factor 1 and linear consistency in the chord (vm execution).
