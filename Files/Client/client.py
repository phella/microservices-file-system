import zmq
import sys
import random
import time
import os
import cv2 
import up_down
import sys
sys.path.append('../')
from utility import log , remove_log

remove_log()
port = 5556
context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
for i in range(3):
    socket.connect ("tcp://10.8.0.34:%s" % str(port + i))
client_id = random.randrange(1,10005)


context = zmq.Context()
socketDk = context.socket(zmq.REQ)

# i need to upload/download a video ask tracker
def askTracker(type , filename):
    socket.send_pyobj ({"type":type , "file":filename})
    log(" Request of type" + type + " sent")
    #  Get the reply of the DK and port no of it to communicate. 
    message = socket.recv_pyobj()
    print(message)
    log(" Response recieved with ip" + message["ips"][0] + " port number " +message["ports"][0])
    return message

def makeConnections(ports,ips):
    for i in range (len(ports)):
        socketDk.connect(ips[i] +  ports[i])
        log(" Client connected to data keeper")

def main(type , filename):
    message = askTracker(type ,filename)
    ports = message["ports"]
    ips = message["ips"]
    makeConnections( ports , ips ) 
    if type == "upload":
        up_down.upload(socketDk,filename)
        log("File uploaded successfully")
    else:
        up_down.download(socketDk,filename)
        log("File downloaded successfully")

main(sys.argv[1] ,  sys.argv[2])