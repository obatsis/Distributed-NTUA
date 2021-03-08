import requests
import os
from PyInquirer import style_from_dict, Token, prompt


baseURL = 'http://localhost:5000/cli'

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '#0bf416',
    Token.Answer: '#2196f3 bold',
    Token.Question: '#0bf416 bold',
})

def red(string):
    return '\033[1;91m {}\033[00m\n'.format(string)

def yellow(string):
    return '\033[1;93m {}\033[00m\n'.format(string)

def client():
    os.system('cls||clear')
    yellow('What a beautiful day to enter the cult...')
    while True:
        print('----------------------------------------------------------------------')
        method_q = [
            {
                'type': 'list',
                'name': 'method',
                'message': 'Select action:',
                'choices': ['Join', \
                            'Depart', \
                            'Insert', \
                            'Delete', \
                            'Query', \
                            'Overlay', \
                            'Help', \
                            'Exit']
            }]
        method_a = prompt(method_q, style=style)['method']
        # os.system('cls||clear')

        if method_a == 'Join':
            print("Node join")

            joinURL = "joinURL"
            endpoint = baseURL + joinURL
            # response = requests.get(endpoint)

            continue

        elif method_a == 'Depart':
            print("Node departure")

            departURL = "departURL"
            endpoint = baseURL + departURL
            # response = requests.get(endpoint)
            continue

        elif method_a == 'Insert':
            print('Insert key-value pair')
            
            insertURL = "departURL"
            endpoint = baseURL + insertURL
            # response = requests.post(endpoint)

            continue

        elif method_a == 'Delete':
            print('Delete key')
            
            deleteURL = "deleteURL"
            endpoint = baseURL + deleteURL
            # response = requests.post(endpoint)

            continue

        elif method_a == 'Query':
            print('Query key')

            queryURL = "queryURL"
            endpoint = baseURL + queryURL
            # response = requests.post(endpoint)

            continue


        elif method_a == 'Overlay':
            print('Overlay key')
            
            overlayURL = "overlayURL"
            endpoint = baseURL + overlayURL
            # response = requests.get(endpoint)

            continue

        elif method_a == 'Help':
            print('---- Help ----\n')
            
            joinHelp="joinHelp"
            departHelp="departHelp"
            insertHelp="insertHelp"
            deleteHelp="deleteHelp"
            queryHelp="queryHelp"
            overlayHelp="overlayHelp"

            print(" -",joinHelp,"\n",\
                  "-",departHelp,"\n",\
                  "-",insertHelp,"\n",\
                  "-",deleteHelp,"\n",\
                  "-",queryHelp,"\n",\
                  "-",overlayHelp,"\n"
                  )

            continue

        elif method_a == 'Exit':
            os.system('cls||clear')
            
            break

        else:
            break

if __name__ == '__main__':

    client()
