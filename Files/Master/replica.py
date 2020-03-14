import sys
import zmq
import time
from utility  import log 
port = "7000"
sockets=[]
context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
def replica( no_of_datakeepers , num_of_replicas , status , lookup , freeports , ips ):
    log(str(no_of_datakeepers))
    log(str(num_of_replicas))
    for i in range(no_of_datakeepers):
        zmq_socket.bind("tcp://*:%s" % str(int(port)+i))
        sockets.append(zmq_socket)
    while True:
        keys = lookup.keys()
        for file in keys:
            nodes = lookup[file]
            x=0
            used = {0}
            used.clear()
            for node in nodes:
                used.add(node)
                if(status[int(node)]):
                    x += 1
            repeat(file , used , status , lookup , freeports , ips , x , num_of_replicas)
        time.sleep(10)

def repeat(index, used , status , lookup , freeports , ips , count , num_of_replicas):# index of the file in the lookup table
    free_keepers = [x for x in range(len(status)) if x not in used]
    log("repeat function called")
    for i in free_keepers:  #checking until find a datakeeper free of my file

            if( count >= num_of_replicas):
                break
            if(status[i] == 1): #the datakeeper is alive
                count += 1
                lis = []
                lis2 = []
                c=0
                while c < 1 :
                    try:
                        x = freeports[i].pop(0)
                        lis.append(x)
                        lis2.append(ips[i])
                        c += 1
                    except:
                        break
                for j in used:
                    if(status[j]==1):
                        sockets[j].send_pyobj({"ports":lis, "ips":lis2,"filename":index})
                        break
