import sys
import zmq
from multiprocessing import Process, Array , Manager
from utility import log 

def tracker(id , port ,  status_table , lookup_table , free_ports):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    while True:
    #  Wait for next request from client
        message = socket.recv_pyobj() 
        if(message["type"] == "download"):
            lis = []
            try :
                x = free_ports.pop(0)
                lis.append(x)
                x = free_ports.pop(0)
                lis.append(x)
            socket.send_pyobj({"ports":lis})
