
'''
Hello! I'm a node!
If you want talk with me you have to use the following endpoints

# Discover another node
Q: /hello!
A: 200!

# How old are you?
Q: /how old are you?
A: {im:0.0.1}

# Know him
Q: /who are you? I'm {name, address}
A: [{My name is}]
   /who are you?

# Share friends
Q: Do you have friends?
A: [{My friend name is, and his number is }]

# Chat with friend
Q: /hey!
A: [{Hi mate!}]

# Leave him
Q: /goodbye

'''
version = '0.0.1'

from optparse import OptionParser
from flask import Flask, jsonify, request
import requests
import threading
import json

class HumanNode():
    def __init__(self):
        self.name = str
        self.address = str
        self.age = {'im':version}
        self.friends = []

        self.newFriend = str


# that`s me ... node!
node = HumanNode()

# And this is the REST
RESTofTheWorld = Flask(__name__)

@RESTofTheWorld.route('/hello')
def hello():
    return '',200

@RESTofTheWorld.route('/howoldareyou')
def HowOldAreYou():
    return jsonify(node.age),200

@RESTofTheWorld.route('/whoareyou', methods=['GET', 'POST'])
def WhoAreYou():
    if request.method == 'POST':
        print request.json
        print("I have new friend %s @ %s!" %(request.json.get('name'),request.json.get('address')))
        return jsonify({'name': node.name, 'address': node.address })
    if request.method == 'GET':
        return jsonify({'name': node.name, 'address': node.address })

def runRESTofTheWorld():
    RESTofTheWorld.run(host=node.address.split(":")[0],port="5000" \
        if node.address.split(":").__len__() <= 1 else node.address.split(":")[1])


#
def sayHello():
    try:
        r = requests.get("http://"+str(node.newFriend)+"/hello")
        return [r.status_code,r.text]
    except requests.ConnectionError:
        return [0]

def askAge():
    question = "/howoldareyou"
    r = requests.get("http://" + str(node.newFriend)+ question)
    return [r.status_code, r.json]

def askWhoIs():
    question = "/whoareyou"
    header = { 'Content-Type': 'application/json' }
    r = requests.post("http://" + str(node.newFriend) + question,
                    data=json.dumps({ 'name': node.name, 'address': node.address }),
                    headers=header)
    return [r.status_code, r.json]

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-n", "--name", dest="name",
                      help="Choose node name")
    parser.add_option("-a", "--address", dest="address", default="127.0.0:8080",
                      help="Set node address")
    parser.add_option("-k", "--know", dest="know",
                      help="Declare your friend")

    (options, args) = parser.parse_args()
    node.name = options.name
    node.address = options.address
    if options.know is not None:
        node.newFriend = options.know
    print("My name is %s, I'm %s years old and my address is %s \nI have %d friend%s"
          %(node.name, node.age['im'], node.address,node.friends.__len__(),
            "s" if node.friends.__len__() > 1 else " :(",))
    print("I wanna know %s" %(node.newFriend))
    rotw = threading.Thread(target=runRESTofTheWorld)
    rotw.start()
    if node.newFriend is not None:
        friend = HumanNode()
        if sayHello()[0] == 200:
            print "One node!"
            age = askAge()
            if age[0] == 200:
                print friend.age
                if friend.age['im'] == node.age['im']:
                    print "We have the same age!"

                    who = askWhoIs()
                    print who
                    if who[0] == 200:
                        print ("I have new friend!")