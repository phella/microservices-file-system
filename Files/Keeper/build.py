# takes id of the data_keeper

import subprocess
import importlib
import os
import sys
from multiprocessing import Process
from utility import remove_log
from data_keeper import Keeper
from isAlive import alive 
from dummyClient import dummyClient

id =0
remove_log()
n = 3
# run same data keeper many times
for i in range(0,n):
    p0 = Process(target = Keeper , args = ( str(i) , str(5700+i)) )
    p0.start()


p0 = Process(target = alive , args = ( id ,  str(6000)) )
p0.start()
p0.join()