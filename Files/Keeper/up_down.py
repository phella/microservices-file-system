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
    print("im here about to upload")
    log("File readed successfully")
    socketDk.send_pyobj({"type":"upload","file":rd, "filename":file})
    print("i have just sent")
    log("File sent successfully")
    f.close()
    # return socketDk.recv_pyobj()
    return "successful uploading"

def download (socketDk,file ,filename):
    f = open(filename , 'wb')
    f.write(file)
    f.close()
    socketDk.send_string("succeful uploading")