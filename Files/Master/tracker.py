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
        if(message["type"] == "upload"):
            lis = []
            lis2 = []
            count = 0
            while count < 1 :
                try:
                    x = free_ports[counter].pop(0)
                    lis.append(x)
                    lis2.append(ips[counter])
                    count += 1
                    counter = (counter + 1)% no_keepers
                except:
                    
            socket.send_pyobj({"ports":lis , "ips" : lis2})
        else if( message["type" ] == "download"):
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
            
            socket.send_pyobj({"ports":lis, "ips":lis2})

