# Τεραστιο ενδεχομενο να εχω λουσει....

import sys
import os
from flask import Flask, request, render_template
import werkzeug
import requests
import hashlib
import config
from api import *
from utils.beautyfy import *

app = Flask(__name__)
address = 'http://localhost:'
matrix_of_items = [] # matrix of pairs(key,value)
self_ID = '...' # το IP του εκάστοτε node
previous_ID = None
next_ID = None
initial_node = False # αν ειναι ο αρχικος κομβος πρεπει να ειναι True
node_in_chord = True # there is the node in chord
----------

def hash(key):
    return hashlib.sha1(key.encode('utf-8')).hexdigest()

def found(matrix_of_items, key):
    for item in matrix_of_items:
        if item[0] == key:
            return(item)

@app.route('/insert', methods = ['GET'])
def chord_insert():
    if request.method == 'GET':
        args = request.args # args is a pair of (key,value)
        print(args)
        hashed_key = hash(args['key'])
        command = 'insert'
        if(hashed_key > hash(previous_ID) and hashed_key <= hash(self_ID)):
            item = found(matrix_of_items, args['key'])
            if(item): # update
                matrix_of_items.remove(item)
            matrix_of_items.append((args['key'], args['value'])) # inserts the updated pair of (key,value)
            print('Updated!')
            print(matrix_of_items)
            return "Inserted by node" + self_ID
        elif((hashed_key > hash(self_ID) and initial_node and hashed_key > hash(previous_ID)) or (hashed_key < hash(previous_ID) and initial_node and hashed_key <= hash(self_ID))):
            item = found(matrix_of_items, args['key'])
            if(item): # update
                matrix_of_items.remove(item)
            matrix_of_items.append((args['key'], args['value'])) # inserts the updated pair of (key,value)
            print('Updated!')
            print(matrix_of_items)
            return "Inserted by node" + self_ID
        elif(hashed_key > hash(self_ID) or hashed_key < hash(previous_ID)):
            print('forwarding..')
            tuple_load = {'key':args['key'], 'value':args['value']}
            req = requests.get(url = 'http://' + next_ID + '/insert', params = tuple_load)
            return req.content.decode("utf-8")
        print("Insersion from server is done!")

@app.route('/delete',methods = ['GET'])
def chord_delete():
    if request.method == 'GET':
        args = request.args # args is a pair of (key,value)
        print(args)
        hashed_key = hash(args['key'])
        command = 'delete'
        if(hashed_key > hash(previous_ID) and hashed_key <= hash(self_ID)):
            item = found(matrix_of_items, args['key'])
            if(item):
                matrix_of_items.remove(item)
            print('Deleted!')
            print(matrix_of_items)
            return "Removed by node" + self_ID
        elif((hashed_key > hash(self_ID) and initial_node and hashed_key > hash(previous_ID)) or (hashed_key < hash(previous_ID) and initial_node and hashed_key <= hash(self_ID))):
            item = found(matrix_of_items, args['key'])
            if(item):
                matrix_of_items.remove(item)
            print('Deleted!')
            print(matrix_of_items)
            return "Removed by node" + self_ID
        elif(hashed_key > hash(self_ID) or hashed_key < hash(previous_ID)):
            print('forwarding..')
            tuple_load = {'key':args['key'], 'value':args['value']}
            req = requests.get(url = 'http://' + next_ID + '/delete', params = tuple_load)
            return req.content.decode("utf-8")
        print("Deletion from server is done!")

@app.route('/query',methods = ['GET'])
def chord_query():
    if request.method == 'GET':
        args = request.args
        command = 'query'
        if(node_in_chord == False):
            return 'NodeIsDown'
        if(args['key'] == '*'):
            return (json.dumps({'matrix_of_items':matrix_of_items}))
        else:
            hashed_key = hash(args['key'])
            if(hashed_key > hash(previous_ID) and hashed_key < hash(self_ID)):
                item = found(matrix_of_items, args['key'])
                print('It is found..')
                print(item)
                return json.dumps(item)
            elif((hashed_key > hash(self_ID) and initial_node and hashed_key > hash(previous_ID)) or (hashed_key < hash(previous_ID) and initial_node and hashed_key <= hash(self_ID))):
                item = found(matrix_of_items, args['key'])
                print('It is found..')
                print(item)
                return json.dumps(item)
            elif(hashed_key > hash(self_ID) or hashed_key < hash(previous_ID)):
                print('forwarding..')
                tuple_load = {'key':args['key']}
                req = requests.get(url = 'http://' + next_ID + '/query', params = tuple_load)
                return req.content.decode("utf-8")

@app.route('./update', methods = ['GET'])
def chord_update():
    global next_ID, previous_ID
    print(previous_ID)
    if request.method == 'GET':
        args = request.args
        if(args['previous']!='n'): previous_ID = args['previous']
        if(args['next']!='n'): next_ID = args['next']
    print('previous = ', previous_ID, 'next = ', next_ID)
    return(previous_ID)

@app.route('/depart',methods = ['GET'])
def chord_depart():
    global next_ID, previous_ID
    global node_in_chord
    args = request.args
    print(args)
    hashed_ID = hash(args['id'])
    node_in_chord = False
    tuple_load = {'previous':previous_ID, 'next':'n'}
    req = requests.get(url = 'http://' + next_ID + '/update', params = tuple_load)
    tuple_load = {'previous':'n', 'next':next_ID}
    req = requests.get(url = 'http://' + previous_ID + '/update', params = tuple_load
    new_list_to_be_send = []
    for item in matrix_of_items:
        new_list_to_be_send.append(item)
        matrix_of_items.remove(item)
    for item in new_list_to_be_send:
        tuple_load = {'key':item[0], 'value':item[1]}
        # insert the pairs of (key,value) in the next_ID's matrix_of_items
        req = requests.get(url = 'http://' + next_ID + '/insert', params = tuple_load)
    return req.content.decode("utf-8")
