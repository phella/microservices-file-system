import sys
import zmq
from multiprocessing import Process, Array , Manager
from utility import log
import random

def tracker(id , no_keepers , ips , port ,  status_table , lookup_table , free_ports):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    counter = 0
    while True:
    #  Wait for next request from client
        message = socket.recv_pyobj()
        log(" Client request " + message["type"] +" filename " + message["file"] , str(id)) 
        if(message["type"] == "upload"):
            lis = []
            lis2 = []
            count = 0
            while count < 1 :
                try:
                    temp = free_ports[counter]
                    x = str(temp.pop(0))
                    free_ports[counter] = temp
                    lis.append(x)
                    lis2.append(str(ips[counter]))
                    count += 1
                    counter = (counter + 1)% no_keepers
                except:
                    pass
            socket.send_pyobj({"ports":lis , "ips" : lis2})
            log(" Respond to upload request" , str(id))
        elif( message["type" ] == "download"):
            filename = message["file"]
            nodes = lookup_table[filename]
            y = random.choice(nodes)
            while(not status_table[y]):
                y = random.choice(nodes)
            lis = []
            lis2 = []
            while count < 1 :
                try:
                    x = free_ports[y].pop(0)
                    lis.append(x)
                    lis2.append(ips[y])
                    count += 1
                except:
                    y = random.choice(nodes)
            socket.send_pyobj({"ports":lis, "ips":lis2})
            log(" Respond to upload request" , str(id))