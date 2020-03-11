import zmq
import sys
import time

import up_down

context = zmq.Context()
socketDk = context.socket(zmq.REQ)

def makeConnections(ports, ips):
    for i in range(len(ports)):
        socketDk.connect(ips[i]+":%s" % ports[i])


def dummyClient(port):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://192.168.110.134:%s" % port)
    context = zmq.Context()
    socketDk = context.socket(zmq.REQ)

    while True:
        message=socket.recv_pyobj()
        ports=message["ports"]
        ips=message["ips"]
        makeConnections(ports, ips)
        up_down.upload(socketDk,message["filename"])
