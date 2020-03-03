import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % "6000")
socket.connect ("tcp://localhost:%s" % "6001")
socket.connect ("tcp://localhost:%s" % "6002")

def download(userid , filename):
    socket.send_pyobj ({"type":"download","userid":userid , "filename":filename})
    message = socket.recv_pyobj()


