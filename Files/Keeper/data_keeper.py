import zmq
import random
import sys
import time

import up_down as up_down

#pair connection to serve client upload/download
def Keeper(id,port2):
    context = zmq.Context()
    socket2 = context.socket(zmq.REP)
    socket2.bind("tcp://*:%s" % port2)

    # socket2.send/("Server message to client3")
    message = socket2.recv_pyobj()
    if(message["type"]=="download"):  #download
        up_down.upload(socket2,message["file"])
    else : #upload
        up_down.download(socket2,message["file"])
    time.sleep(1)

    #tell master tracker i've finished U/D file...
    socket2.send_pyopbj({"msg":"successfull_work","file" : None,"type":message["type"]})
