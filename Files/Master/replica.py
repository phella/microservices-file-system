
def replica(num_of_replicas,status,lookup,freeports):
    while True:
        keys = Dictionary1.keys()
        for file in keys:
            nodes = lookup[file]
            x=0
            used = {0}
            used.clear()
            for node in nodes:
                used.add(node)
                if(status[node]):
                    x += 1
                repeat(file , used , status , lookup , freeports,x,num_of_replicas)
        sleep(10)

def repeat(index, used , status , lookup,freeports,count,num_of_replicas):# index of the file in the lookup table
    free_keepers = [x for x in range(len(status)) if x not in used]
    for i in free_keepers:  #checking until find a datakeeper free of my file
            if( count > num_of_replicas):
                break
            if(status[i] == 1): #the datakeeper is alive
                count += 1
                #download  here i need  hamdyyyyyyyy
