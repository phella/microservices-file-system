import zmq 
import sys
import time
import os
import signal
import threading
from utility import log

ips = [
    'tcp://127.0.0.1:',
    'tcp://127.0.0.2:',
    'tcp://127.0.0.3:',
    'tcp://127.0.0.4:'
]
pids = [
    -1,
    -1,
    -1,
    -1
]

master_pid = -1
master_id = -1

def claim(signum , dummy):
    global master_pid,master_id,pids,my_id,in_election
    in_election = False
    master_pid = pids[my_id]
    master_id = my_id
    socket.send_string('victory '+str(my_id) + ' ' + str(pids[my_id]))
    t1 = threading.Thread(target=master)
    t1.start()
    listen() 


def master():
    global master_pid,pids,my_id,socket
    log("I am the new master with id = " + str(my_id))
    while(1):
        if(master_pid == pids[my_id]):
            socket.send_string("alive " + str(my_id)+ " "  + str(pids[my_id]))
            time.sleep(1)

def start_election(signum , dummy):
    log("Election started")
    global pids,my_id,socket,in_election
    in_election = True
    candidates = [i for i in pids if i >= pids[my_id]]
    for candidate in candidates:
        socket.send_string(str(candidate) + " " + str(my_id) + " " + str(pids[my_id]))
    signal.signal(signal.SIGALRM, claim)
    signal.alarm(5)


def listen():
    global socket2,master_id,master_pid,pids,in_election,socket
    while(1):
        message = socket2.recv_string()
        topic , _id ,pid = message.split()
        pids[int(_id)] = int(pid)   # store other processes PIDs
        if(topic == "alive" and master_id != -1):
            log(str(my_id) + " Recieved alive message from master: ' " + message +" '")
            signal.signal(signal.SIGALRM, start_election)
            signal.alarm(2)
        elif(topic == "victory"):
            log(str(my_id) + " Recieved victory message from master: ' " + message +" '")
            in_election = False
            signal.signal(signal.SIGALRM, start_election)
            signal.alarm(2)
            master_id = int(_id)
            master_pid = int(pid)
        elif(topic == str(pids[my_id])):
            if(pids[my_id] > int(pid)):
                log(str(my_id) + " Recieved election message from smaller: ' " + message +" '")
                socket.send_string(pid + " " + str(my_id) + " " + str(pids[my_id]))
                if( not in_election):
                    start_election(-1,-1)
            else:
                log(str(my_id) + " Recieved wait message from bigger: ' " + message +" '")
                signal.signal(signal.SIGALRM, start_election)
                signal.alarm(10)
        elif(topic == "awake"):
                log(str(my_id) + " Recieved awake message from new node: ' " + message +" '")
                pids[int(_id)] = int(pid)
                if( not in_election):
                    start_election(-1,-1) 
        

in_election = True
my_id = int(sys.argv[1])
pids[my_id] = os.getpid()
log("Process " + str(my_id) + " started with pid = " + str(pids[my_id]))

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(ips[my_id]+'3000')

socket2 = context.socket(zmq.SUB)
for ip in ips:
    if (ip != ips[my_id]):
        socket2.connect(ip+'3000')

socket2.setsockopt_string(zmq.SUBSCRIBE, "awake")
socket2.setsockopt_string(zmq.SUBSCRIBE, "alive")
socket2.setsockopt_string(zmq.SUBSCRIBE, "victory")
socket2.setsockopt_string(zmq.SUBSCRIBE, str(pids[my_id]))

time.sleep(1)
socket.send_string('awake ' + str(my_id) + ' ' + str(pids[my_id]))

signal.signal(signal.SIGALRM, claim)
signal.alarm(2)
listen()
