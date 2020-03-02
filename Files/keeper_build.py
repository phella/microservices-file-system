import subprocess
import os
import sys
from utility import remove_log


remove_log()
n = int(sys.argv[1])


# run same data keeper many times
for i in range(0,n):
    subprocess.Popen(["python","data_keeper_alive.py", "1" , str(5556 + i) ])
