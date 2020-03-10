import zmq
import sys
import time
import up_down
sys.path.insert(1, "../../")
# import Files.up_down as up_down
import Files.client

def dummyClient(port):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%s" % port)
    while True:
        message=socket.recv_pyobj()
        ports=message["ports"]
        ips=message["ips"]
        makeConnections(ports,ips)
        up_down.upload(socketDk,message["filename"])
