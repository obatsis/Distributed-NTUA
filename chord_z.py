# Τεραστιο ενδεχομενο να εχω λουσει....

import sys
import os
import json
from flask import Flask, request, render_template
import werkzeug
import requests
import hashlib
import config
from api import *
from utils.beautyfy import *

app = Flask(__name__)
# address = 'http://localhost:'
# global songs = [] # matrix of pairs(key,value)

----------

def hash(key):
    return hashlib.sha1(key.encode('utf-8')).hexdigest()

def found(globs.songs, key):
    for item in globs.songs:
        if item[0] == key:
            return(item)

@app.route('/chord/insert', methods = ['POST'])
def chord_insert():
    if request.method == 'POST':
        args = request.form.to_dict() # args is a pair of (key,value)
        print(args)
        hashed_key = hash(args["key"])
        command = 'insert'
        previous_ID = globs.mids[0]["uid"]
        next_ID = globs.mids[1]["uid"]
        self_ID = globs.my_id
        # δεν θεωρω οτι το id ειναι χασαρισμενο...
        if(hashed_key > previous_ID and hashed_key <= self_ID):
            item = found(globs.songs, args["key"])
            if(item): # update
                globs.songs.remove(item)
            globs.songs.append({"key":args["key"], "value":args["value"]}) # inserts the updated pair of (key,value)
            print('Updated!')
            print(globs.songs)
            return "Inserted by node" + self_ID
        elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
            item = found(globs.songs, args["key"])
            if(item): # update
                globs.songs.remove(item)
            globs.songs.append({"key":args["key"], "value":args["value"]}) # inserts the updated pair of (key,value)
            print('Updated!')
            print(globs.songs)
            return "Inserted by node" + self_ID
        elif(hashed_key > self_ID or hashed_key < previous_ID):
            print('forwarding..')
            tuple_load = {"key":args["key"], "value":args["value"]}
            result = requests.post(config.ADDR + globs.mids[1]["ip"] + ":" + globs.mids[1]["port"] + "/chord/insert", data = tuple_load)
            # req = requests.get(url = 'http://' + next_ID + '/insert', params = tuple_load)
            return result.content.decode("utf-8")
        print("Insersion from server is done!")

@app.route('/chord/delete',methods = ['POST'])
def chord_delete():
    if request.method == 'POST':
        args = request.form.to_dict() # args is a pair of (key,value)
        print(args)
        hashed_key = hash(args["key"])
        previous_ID = globs.mids[0]["uid"]
        next_ID = globs.mids[1]["uid"]
        self_ID = globs.my_id
        command = 'delete'
        # δεν θεωρω οτι το id ειναι χασαρισμενο...
        if(hashed_key > previous_ID and hashed_key <= self_ID):
            item = found(globs.songs, args["key"])
            if(item):
                globs.songs.remove(item)
            print('Deleted!')
            print(globs.songs)
            return "Removed by node" + self_ID
        elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
            item = found(globs.songs, args["key"])
            if(item):
                globs.songs.remove(item)
            print('Deleted!')
            print(globs.songs)
            return "Removed by node" + self_ID
        elif(hashed_key > self_ID or hashed_key < previous_ID):
            print('forwarding..')
            tuple_load = {"key":args["key"], "value":args["value"]}
            result = requests.post(config.ADDR + globs.mids[1]["ip"] + ":" + globs.mids[1]["port"] + "/chord/delete", data = tuple_load)
            # req = requests.get(url = 'http://' + next_ID + '/delete', params = tuple_load)
            return result.content.decode("utf-8")
        print("Deletion from server is done!")

@app.route('/chord/query',methods = ['POST'])
def chord_query():
    if request.method == 'POST':
        args = request.form.to_dict()
        command = 'query'
        previous_ID = globs.mids[0]["uid"]
        next_ID = globs.mids[1]["uid"]
        self_ID = globs.my_id
        if(node_in_chord == False):
            return 'NodeIsDown'
        if(args["key"] == '*'):
            return (json.dumps({'matrix_of_items':matrix_of_items}))
        else:
            hashed_key = hash(args["key"])
            # δεν θεωρω οτι το id ειναι χασαρισμενο...
            if(hashed_key > previous_ID and hashed_key < self_ID):
                item = found(globs.songs, args["key"])
                print('It is found..')
                print(item)
                return json.dumps(item)
            elif((hashed_key > self_ID and hashed_key > previous_ID) or (hashed_key < previous_ID and hashed_key <= self_ID)):
                item = found(globs.songs, args["key"])
                print('It is found..')
                print(item)
                return json.dumps(item)
            elif(hashed_key > self_ID or hashed_key < previous_ID):
                print('forwarding..')
                tuple_load = {"key":args["key"]}
                result = requests.post(config.ADDR + globs.songs[1]["ip"] + ":" + globs.songs[1]["port"] + "/chord/query", data = tuple_load)
                # req = requests.get(url = 'http://' + next_ID + '/query', params = tuple_load)
                return result.content.decode("utf-8")


@app.route('/help', methods = ['GET'])
def help():
    help_dictionary = {'join': '-----',
                       'depart': '-----',
                       'insert': '-----',
                       'delete': '-----',
                       'query': '-----',
                       'update': '-----',
                       'overlay': '-----'}
    print("Prints a helping message to the user")
    print("+------------------------------------+")
    print("+------------COMMAND LINE------------+")
    print(help_dictionary)
