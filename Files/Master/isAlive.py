import sys
import zmq
import signal
from multiprocessing import Process, Array , Manager
from functools import partial

sys.path.append('../')
from utility import log , remove_log , listToString

keepers = 0 # Number of keepers
current = 0 # Number of alive keepers

def alive( no_keepers , ips , status , lookup_table , free_ports):
    global current
    current = no_keepers     # Number of alive data keepers
    global keepers
    keepers = no_keepers
    active =  {0}      # Every second collect data keepers in set
    active.clear()
    counter = 0      # Every second count data keepers
    signal.signal(signal.SIGALRM, partial(handler ,status))

    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    for i in range(0 , no_keepers):
        socket.connect ( ips[i] + "6000" )  # Connect to isAlive of keepers 

    topicfilter = "isALive"
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    
    while(True): 
        signal.alarm(2)         # After 2 seconds all Processes are dead
        state = socket.recv_string()
        topic , id = state.split()
        id = int(id)
        active.add( id )
        if(status[ id ] == 0):         # Dead data keeper return back alive
            current += 1
            status[id] = 1
            log(" Data keeper is back")
        counter += 1
        if( counter ==  current ):                # 1 sec completed
            if( len(active) != current ):           # Replicated data keeper means 1 data keeper is dead
                log(" Detected dead data keeper")
                for i in range(no_keepers):
                    status[i] = 0
                current = len(active)             # New current number
                for i in range(0 , current):
                    status[active.pop() ] = 1    # Mark active data keepers 
            counter = 0                                 #init counters
            active.clear()
            log(listToString(status))


def handler(status ,signum, frame):
    signal.alarm(2)
    log(" All data keepers are dead")
    global keepers
    global current
    for i in range(keepers):
        status[i] = 0
    current = 0
    log(listToString(status))