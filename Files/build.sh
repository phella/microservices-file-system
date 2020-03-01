#!/bin/bash

# to do remove old log files before new build

#run master parms ( n , ip1 , por1 , ip2 , port2 ) 
python master.py 1 tcp://localhost: 5556

#run slaves
python data_keeper.py
