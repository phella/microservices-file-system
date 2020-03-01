import zmq
import sys
import time

port = sys.argv[2]
id = int(sys.argv[1])

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = 1
    socket.send_string("%s %d %d" % ("isALive", id , 256))
    time.sleep(1)
