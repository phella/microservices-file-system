import subprocess
import os
import sys
from utility import remove_log


remove_log()
n = int(sys.argv[1])

# How to get n ips and ports
# Run master parms ( n , ip1 , por1 , ip2 , port2 ) 
subprocess.Popen(["python","master_alive.py", "2" , "tcp://localhost:" , "5556" , "tcp://localhost:" , "5557" ])


