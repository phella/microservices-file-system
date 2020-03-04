import sys
sys.path.append('../')
import zmq
from multiprocessing import Process, Array , Manager
from utility import log 
from Master.isALive import alive

no_process = 3
portbase = 5556
no_keepers = 1
status = Array('i', [1]*n)  # Status of data keepers
ips = [
    "tcp://127.0.0.1:
]

if __name__ == '__main__':
    with Manager() as manager:
        lookup_table = manager.list()
        free_ports = manager.list()
        p0 = Process(target = alive , args = ( no_keepers , ips , status , lookup_table , free_ports) )
        p1 = Process(target = tracker , args = (1 , status , lookup_table) )
        p2 = Process(target = tracker , args = (2 , status , lookup_table) )
        p3 = Process(target = tracker , args = (3 , status , lookup_table) )
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()