import zmq
import time
import sys
sys.path.append('../')
from utility import log , remove_log


remove_log()
def update_table( port , ips , free_ports , lookup_table ):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    for ip in ips :
        for i in range(3):
            socket.connect (ip + str(int(port)+i))
    log(" Event file started successfully")
    topicfilter = "update"
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        string = socket.recv_string()
        topic , keeper_id , free_port , filename = string.split()
        log(" Recived from keeper_id "+ keeper_id +" filename " + filename + " port free " + free_port)
        temp = free_ports[int(keeper_id)]
        temp.append(free_port)
        free_ports[int(keeper_id)] = temp 
        if filename in lookup_table :
            temp = lookup_table[filename]
            temp.append(keeper_id)
            lookup_table[filename] = temp
        else :
            lookup_table[filename] = [keeper_id]
        print(lookup_table)
