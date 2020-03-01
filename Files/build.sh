#!/bin/bash

# to do remove old log files before new build

#run master parms ( n , ip1 , por1 , ip2 , port2 ) 
python master.py 2 tcp://localhost: 5556 tcp://localhost: 5557 &

#run slaves
for i in {1..2}
do
	python data_keeper.py $i  $(( 5555 + $i)) &
done
