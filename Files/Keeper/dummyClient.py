import zmq
import sys
import time
import up_down
def dummyClient(port):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%s" % port)
    while True:
        socket.recv_pyobj()
        ports=message["ports"]
        ips=message["ips"]
        makeConnections(ports,ips)
        up_down.upload(socketDk,message["filename"])
