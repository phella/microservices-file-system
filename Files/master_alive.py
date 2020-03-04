import sys
import zmq
from multiprocessing import Process, Array , Manager
from utility import log 


def tracker(id,status_table , lookup_table ):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    port = str( 6000 + id)
    socket.bind("tcp://*:%s" % port)
    while True:
    #  Wait for next request from client
        message = socket.recv_pyobj() 
        if(message["type"] == "download"):
            socket.send("World from %s" % port)
    
    #for i in range(len(status_table)):
       # print(status_table[i])
    #lookup_table.append({"A":1})
