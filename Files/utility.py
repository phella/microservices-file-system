import inspect

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
	