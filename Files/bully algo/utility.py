import inspect
import os

def log(str , id = "0"):
	frame = inspect.stack()[1]
	module = inspect.getmodule(frame[0])
	filename = module.__file__
	filename = filename[0:-3] + id
	filename += ".log.txt"
	f = open(filename,"a+")
	f.write(str)
	f.write("\n")

def listToString(s):  
    
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += str(ele) + " "  
    
    # return string   
    return str1  

def remove_log():
	dir_name = os.getcwd()
	test = os.listdir(dir_name)
	for item in test:
		if item.endswith(".txt"):
			os.remove(os.path.join(dir_name, item))
