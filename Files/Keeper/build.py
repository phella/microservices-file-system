# takes id of the data_keeper

import subprocess
import importlib
import os
import sys
sys.path.append('../')
from utility import log , remove_log
from multiprocessing import Process
from data_keeper import Keeper
from isAlive import alive 
from dummyClient import dummyClient


id = int(sys.argv[1])
remove_log()
n = 3
# run same data keeper many times
for i in range(0,n):
    p0 = Process(target = Keeper , args = ( str(i),str(id) , str(5700+i)) )
    p0.start()


p0 = Process(target = alive , args = ( id ,  str(6000)) )
p0.start()
p1 = Process(target = dummyClient)
p1.start()
p0.join()