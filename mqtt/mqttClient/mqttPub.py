import paho.mqtt.client as mqtt
import time
import os
from configparser import SafeConfigParser
import io
import sys, getopt

#init configurable vars
pubTopic = ''
clientId = ''
broker = ''

message = '-'

# help function on exception
def help_me():
    print()
    print('List of valid arguments:')
    print('-b = broker adress')
    print('-m = message')
    print('-p = topic')

#parse any arguments passed on call
pT = ''
pM = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],"p:m:b:", ["pT=","pM=","b="])
except getopt.GetoptError:
    print('Error: invalid argument')
    help_me()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-m', '--pM'):
        message = arg

    elif opt in ('-p','--pT'):
        pubTopic = arg

    elif opt in('-b','--b'): 
        broker = arg

# load config file if no arg form call
configFilepath = os.path.dirname(os.path.realpath(sys.argv[0])) + '/mqttConfig.ini'
config = SafeConfigParser()
config.read(configFilepath)
if pubTopic == '':
    pubTopic = config.get('default', 'pubTopic')
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

print("Connect to: "+broker)
print("Publish to: "+pubTopic)
print("Client ID: "+clientId)
print("")

client = mqtt.Client(clientId) #new instance
client.on_connect = on_connect #bind callback function
client.on_disconnect = on_disconnect

client.connect(broker, 1883)
client.loop_start()
client.publish(pubTopic, message)
time.sleep(1)
client.loop_stop()
client.disconnect()
