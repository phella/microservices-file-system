import zmq
import sys
import time
from utility import log

def alive(id , port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    while True:
        topic = 1
        socket.send_string("%s %d " % ("isALive", id))
        time.sleep(1)
