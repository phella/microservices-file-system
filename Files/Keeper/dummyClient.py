import zmq
import sys
import time

import up_down


def makeConnections(socket , ports, ips):
    for i in range(len(ports)):
        socket.connect(ips[i]+"%s" % ports[i])


def dummyClient():
    context = zmq.Context()
    soc = context.socket(zmq.REQ)
    port = "7000"
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:" + port)
    while True:
        message = socket.recv_pyobj()
        print("recieved el7")
        ports = message["ports"]
        ips = message["ips"]
        makeConnections(soc , ports, ips)
        up_down.upload(soc , message["filename"])
