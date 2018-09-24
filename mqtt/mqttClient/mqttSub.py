import paho.mqtt.client as mqtt
import time
import os
from configparser import SafeConfigParser
import io
import sys, getopt

#init configurable vars
subTopic = ''
clientId = ''
broker = ''
# help function on exception
def help_me():
    print()
    print('List of valid arguments:')
    print('-b = broker adress')
    print('-p = topic')

#parse any arguments passed on call
sT = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],"s:b:", ["sT=","b="])
except getopt.GetoptError:
    print('Error: invalid argument')
    help_me()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-s','--sT'):
        subTopic = arg

    elif opt in('-b','--b'): 
        broker = arg

# load config file if no arg form call
configFilepath = os.path.dirname(os.path.realpath(sys.argv[0])) + '/mqttConfig.ini'
config = SafeConfigParser()
config.read(configFilepath)
if subTopic == '':
    subTopic = config.get('default', 'subTopic')
if clientId == '':
    clientId = config.get('default', 'clientId')
if broker == '':
    broker = config.get('default', 'broker')

#Callbacks
def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connection established...")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnect result code "+str(rc))

def on_message(client, userdata, msg):
    time.sleep(1)
    print(str(msg.payload.decode("utf-8")))

print("Connect to: "+broker)
print("Subscribe to: "+subTopic)
print("Client ID: "+clientId)
print("")

client = mqtt.Client(subTopic) #new instance
client.on_connect = on_connect #bind callback function
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(broker, 1883)
while True:
    client.loop_start()
    client.subscribe(subTopic)
    time.sleep(1)
