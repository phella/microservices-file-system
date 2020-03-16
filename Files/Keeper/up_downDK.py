import zmq
import sys
sys.path.append('../')
from utility import log , remove_log

def upload (socketDk,file):
    f=open(file,'rb')
    rd=f.read()
    log("File readed successfully")
    socketDk.send_pyobj({"type":"upload","file":rd, "filename":file})
    log("File sent successfully")
    f.close()
    return "successful uploading"

def download (socketDk,file ,filename):
    f = open(filename , 'wb')
    f.write(file)
    f.close()
    log("File saved to datakeeper , filename :" + filename)
    socketDk.send_string("succeful uploading")
   
