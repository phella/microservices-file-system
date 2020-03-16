import zmq
import random
import sys
import time
sys.path.append('../')
from utility import log , remove_log

import up_down as up_down

#pair connection to serve client upload/download
def Keeper(processId,keeperId,port2):
    context = zmq.Context()
    socket2 = context.socket(zmq.REP)
    socket2.bind("tcp://*:%s" % port2)
    
    port = "3555"
    context = zmq.Context()
    socket_master = context.socket(zmq.PUB)
    socket_master.bind("tcp://*:" + str( int(port) + int(processId) ) )
    while True :
        # socket2.send/("Server message to client3")
        message = socket2.recv_pyobj()
        if(message["type"] == "download"):  #download
            up_down.upload(socket2 , message["filename"])
            log("File downloaded syccessfully" ,str(keeperId))
        else : #upload
            up_down.download(socket2 , message["file"] , message["filename"])
            log("File uploaded syccessfully" ,str(keeperId))


        #tell master tracker i've finished U/D file...
        # socket2.send_pyopbj({"msg":"successfull_work" , "file" : None , "type":message["type"]})

        socket_master.send_string("update "+str(keeperId)+" "+ message["type"]+" "+str(port2)+" "+str(message["filename"]))
        log(" Sent free ports to master" , str(keeperId))
