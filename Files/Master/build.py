import sys
sys.path.append('../')
import zmq
from multiprocessing import Process, Array , Manager
from utility import log , remove_log
from Master.isALive import alive
from Master.tracker import tracker
from Master.replica import replica
from Keeper.events import update_table

no_process = 3
port_base = 5556
no_keepers = 1
status = Array('i', [1]*n)  # Status of data keepers
ips = [
    "tcp://127.0.0.1:
]

if __name__ == '__main__':
    with Manager() as manager:
        lookup_table = manager.dict()
        free_ports = manager.dict()
        for i in range(3) : 
            free_ports[i] = [ 5700 , 5701 , 5702 ] 
        p0 = Process(target = alive , args = ( no_keepers , ips , status , lookup_table , free_ports) )
        for i in range (no_process):
            p1 = Process(target = tracker , args = (i , ips , str( port_base + i )  ,  status , lookup_table , free_ports) )
            p1.start()
            p1.join()
        p1 = Process( target = replica , args = (no_process,status,lookup_table,free_ports))
        p1.start()
        p2 = Process(target = update_table , args = ( str(3555) , ips , free_ports , lookup_table)  )
        p2.start()