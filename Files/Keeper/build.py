# takes id of the data_keeper

import subprocess
import importlib
import os
import sys
from multiprocessing import Process
sys.path.insert(0,'/home/ahmed/education/3rd year/operating system/2nd term/Drive/Files/')
from utility import remove_log
sys.path.insert(0,'/home/ahmed/education/3rd year/operating system/2nd term/Drive/Files/Keeper/')
from Keeper.data_keeper import Keeper
sys.path.insert(0,'/home/ahmed/education/3rd year/operating system/2nd term/Drive/Files/Keeper/')
from Keeper.isAlive import alive


remove_log()
sys.path.append('Keeper/')
n = 3
# run same data keeper many times
for i in range(0,n):
    p0 = Process(target = Keeper , args = ( str(i) , str(5400+i)) )
    p0.start()


p0 = Process(target = alive , args = (sys.argv[1] ,  str(6000)) )