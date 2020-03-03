import sys
import zmq
from multiprocessing import Process, Value, Array
from utility import log 

port = "5556"
n = int(sys.argv[1]) # Number of data keepers
current = n     # Number of alive data keepers
status = Array('i', [1]*n)  # Status of data keepers
active =  {0}      # Every second collect data keepers in set
active.clear()
counter = 0      # Every second count data keepers
ips = []        # List of data keepers id
ports = []      # List of ports
storage = [1024]*n     # List of free storage on each data keeper


for i in range(0 , 2*n - 1 , 2):
    ips.append(sys.argv[2+i])
    ports.append(sys.argv[3+i])

def tracker(dummy,status_table):
    for i in range(len(status_table)):
        print(status_table[i])



def build_tracker():
    p1 = Process(target = tracker , args = (1,status) )
    p2 = Process(target = tracker , args = (1,status) )
    p3 = Process(target = tracker , args = (1,status) )
    p1.start()
    p2.start()
    p3.start()


build_tracker()


# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

for i in range(0 , n):
    socket.connect (ips[i] + ports[i])

topicfilter = "isALive"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

#I think this should be on thread
while(True): 
    state = socket.recv_string()
    topic , id , size = state.split()
    log("Data keeper " + id + " alive")
    id = int(id)
    active.add(id)
    storage[id - 1 ] = int(size)
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
    