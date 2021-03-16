1. After setting up the machines, enabling your public ip,
and setting up a local network, you have to ssh to master and move the contents
of `/scripts` directory to  all nodes by `sftp`. Then change the
hostnames of each machine, according to `hosts_change.txt`.

2. In each node you have to run `sudo nano /etc/hosts` and copy-paste the contents
of `hosts_changes.txt` under `127.0.1.1	snf-18274`. Save and exit. Repeat for
every machine.

3. Then you have to run `sudo ./nat_master.sh` while in master node
(you have to also run 'sudo chmod +x nat_master' before).

4. Then inside each node you have to run `sudo ./nat_slave.sh` again by running
'sudo chmod +x nat_slave' before.

Now bootstrap operates as a router to all other nodes in order for them to have
access to the internet.

5. If you want to establish passwordless communication between master
and all other nodes, run in master: `sudo chmmod +x set_passwordless_ssh` and
`sudo ./set_passwordless_ssh` and follow the instructions.

6. Now you have to upload via `sftp` the script `/scripts/git_utils.sh` to every
node including master and then upload the script`/scripts/git_pull_nodes.sh`
only to master. Run the script `/scripts/git_pull_nodes.sh` from master.
It should initially clone this repo to every node, and after that by running
it again it sould pull main to every node (including master).

7. Last step before we are ready to run the application is to install all
dependecies. In order to do that, simply run `vm_dependencies.sh` script from master.
