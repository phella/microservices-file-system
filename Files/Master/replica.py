import sys
import zmq
import time
sys.path.append('../')
from utility import log , listToString
port = "7000"
sockets=[]

def replica( no_of_datakeepers , num_of_replicas , status , lookup , freeports , ips ):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    for i in range(no_of_datakeepers):
        zmq_socket.bind("tcp://*:%s" % str(int(port)+i))
        global sockets
        sockets.append(zmq_socket)
    while True:
        keys = lookup.keys()
        for fil in keys:
            log("file name = " , fil)
            nodes = lookup[fil]
            x = 0
            used = {0}
            used.clear()
            for node in nodes:
                if( x >= num_of_replicas):
                    break
                log("node =" ,str(node))
                used.add(int(node))
                if(status[int(node)]):
                    x += 1
            log("x = " + str(x))    
            repeat(fil , used , status , lookup , freeports , ips , x , num_of_replicas)
        time.sleep(10)

def repeat(index, used , status , lookup , freeports , ips , count , num_of_replicas):# index of the file in the lookup table
    free_keepers = [x for x in range(len(status)) if x not in used]
    #log("free_keepers = " , free_keepers)
    for i in free_keepers:  #checking until find a datakeeper free of my file
            if( count >= num_of_replicas):
                break
            if(status[i] == 1): #the datakeeper is alive
                count += 1
                lis = []
                lis2 = []
                temp = freeports[i]
                #print("Free ports =" , freeports[i])
                x = temp.pop(0)
                log("free port =  " + str(x) )
                freeports[i] = temp
                lis.append(x)
                lis2.append(ips[i])
                for j in used:
                    if(status[j] == 1):
                        global sockets
                        log("Sending filename to dummy")
                        sockets[j].send_pyobj({"ports":lis, "ips":lis2,"filename":index})
                        log("Filename sent")
                        break
