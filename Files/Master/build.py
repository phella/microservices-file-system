import sys
import zmq
from multiprocessing import Process, Array , Manager
from tracker import tracker
from isAlive import alive
from replica import replica
from events import update_table

sys.path.append('../')
from utility import log , remove_log

# Remove old logs
remove_log()

no_processes = 3   # No of tracker processes
port_base = 5556   # Port numbers base of tracker nodes
no_keepers = 2    
status = Array('i', [1]*no_keepers)  # Status of data keepers alive or dead
ips = [
    "tcp://127.0.0.1:",         # Array of data keepers arranged with keepers ids 
    "tcp://192.168.43.79:"
]

if __name__ == '__main__':
    with Manager() as manager:
        lookup_table = manager.dict()   # {'filename' : [kepeer_ids] }
        free_ports = manager.dict()     # { keeper_id : [free_ports] }
        log("Shared memory created successefully")
        for i in range(3) : 
            free_ports[i] = [ 5700 , 5701 , 5702 ] 
        p0 = Process(target = alive , args = ( no_keepers , ips , status , lookup_table , free_ports) )
        p0.start()
        for i in range (no_processes):
            p1 = Process(target = tracker , args = (i , no_keepers , ips , str( port_base + i )  ,  status , lookup_table , free_ports) )
            p1.start()
        p1 = Process( target = replica , args = (no_keepers , 2 , status,lookup_table , free_ports , ips))
        p1.start()
        p2 = Process(target = update_table , args = ( str(3555) , ips , free_ports , lookup_table)  )
        p2.start()
        p0.join()
        p1.join()
        p2.join()