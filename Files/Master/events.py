import zmq
import time
import sys

def update_table( port , ips , free_ports , lookup_table ):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    for ip in ips :
        socket.connect (ip + port)
    topicfilter = "update"
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        string = socket.recv_string()
        topic , id , port , filename = string.split()
        free_ports[id].append(port)
        if filename in lookup_table :
            lookup_table["filename"].append(id)
        else :
            lookup_table["filename"] = [id]


