import zmq
import sys
import time
sys.path.insert(1, '../../Files')

import up_down
sys.path.insert(1, "../../")
# import Files.up_down as up_down
import Files.client

def dummyClient(port):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%s" % port)
    context = zmq.Context()
    socketDk = context.socket(zmq.REQ)

    while True:
        message=socket.recv_pyobj()
        ports=message["ports"]
        ips=message["ips"]
        socketDk=makeConnections(ports, ips)
        up_down.upload(socketDk,message["filename"])


    def makeConnections(ports, ips):
        for i in range(len(ports)):
            socketDk.connect("tcp://"+ips[i]+":%s" % port[i])
