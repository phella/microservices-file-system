import zmq
import sys
import random
import time
import os
import cv2 
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



def download (socketDk,file):
    socketDk.send_pyobj({"type":"download","filename":file})
    ret=socketDk.recv_pyobj()
    f=open(file,'wb')
    f.write(ret["file"])
    f.close()