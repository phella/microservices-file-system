import zmq
import sys
import time

import up_down


def makeConnections(ports, ips,message):
    for i in range(len(ports)):
        context = zmq.Context()
        soc = context.socket(zmq.REQ)
        soc.connect(ips[i]+"%s" % ports[i])
        up_down.upload(soc , message["filename"])


def dummyClient():
    port = "7000"
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:" + port)
    while True:
        message = socket.recv_pyobj()
        print(message)
        print("recieved el7")
        ports = message["ports"]
        ips = message["ips"]
        makeConnections(ports, ips,message)
