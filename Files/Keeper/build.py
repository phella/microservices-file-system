# takes id of the data_keeper

import subprocess
import os
import sys
from multiprocessing import Process
sys.path.append('../')
from utility import remove_log
from Keeper.keeper import keeper
from Keeper.isAlive import 


remove_log()
sys.path.append('Keeper/')
n = 3
# run same data keeper many times
for i in range(0,n):
    p0 = Process(target = keeper , args = ( str(i) , str(5400+i)) )
    p0.start()


p0 = Process(target = alive , args = (sys.argv[1] ,  str(6000)) )