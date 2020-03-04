import sys
sys.path.append('../')
import zmq
from multiprocessing import Process, Array , Manager
from utility import log 

def alive( no_keepers , ips , status , lookup_table , free_ports):
    current = n     # Number of alive data keepers
    active =  {0}      # Every second collect data keepers in set
    active.clear()
    counter = 0      # Every second count data keepers

    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    for i in range(0 , n):
        socket.connect ( ips[i] + "6000" )

    topicfilter = "isALive"
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    
    while(True): 
        state = socket.recv_string()
        topic , id = state.split()
        log("Data keeper " + id + " alive")
        id = int(id)
        active.add(id)
        if(status[ id - 1 ] == 0):         # Dead data keeper return back alive
            current += 1
        counter += 1
        if( counter ==  current ):                # 1 sec completed
            if(len(active) != current):           # Replicated data keeper means 1 data keeper is dead
                status = [0] * n
                current = len(active)             # New current number
                for i in range(0 , current):
                    status[active.pop() - 1 ] = 1    # Mark active data keepers 
            counter = 0                                 #init counters
            active.clear()