import zmq
import sys
import random
import time
import os
import cv2 
# import up_down


port = "5559"
context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
client_id = random.randrange(1,10005)


context = zmq.Context()
socketDk = context.socket(zmq.REQ)

# i need to upload/download a video ask tracker
def askTracker(type):
    socket.send_pyobj ({"type":type})
    #  Get the reply of the DK and port no of it to communicate. 
    message = socket.recv_pyobj()
    return message

def makeConnections(ports,ips):
    for i in range (len(ports)):
        socketDk.connect("tcp://"+ips[i]+":%s" % port[i])

def main():
    type= sys.argv[2]  #take upload or download
    file= sys.argv[3]  #take upload or download
    message=askTracker(type)
    ports=message["ports"]
    ips=message["ips"]
    makeConnections(ports,ips)
    if type=="upload":
        print(up_down.upload(socketDk,file))
    else:
        up_down.download(socketDk,file)

