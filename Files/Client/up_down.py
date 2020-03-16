import zmq
import sys
import random
import time
import os
import cv2 
sys.path.append('../')
from utility import log , remove_log

def upload (socketDk,file):
    # cap =cv2.cv2.VideoCapture(file) #path of the file
    # fps= cap.get(cv2.cv2.CV_CAP_PROP_FPS)
    # frame_width = int (cap.get(3))
    # frame_height = int (cap.get(4)) 
    # success,image = cap.read()
    # socketDk.send_pyobj({"type":"upload","file":file,"protocol":[fps,frame_width,frame_height]})
    # while(success):
    #     socketDk.send_pyobj({"frame":image})
    #     success,image = cap.read()
    # return socketDk.recv_pyobj()
    f=open(file,'rb')
    rd=f.read()
    log("File readed successfully")
    socketDk.send_pyobj({"type":"upload","file":rd, "filename":file})
    log("File sent successfully")
    f.close()
    # return socketDk.recv_pyobj()
    return "successful uploading"



def download (socketDk,file):
    socketDk.send_pyobj({"type":"download","file":file})
    ret=socketDk.recv_pyobj()
    f=open(file,'wb')
    f.write(ret["file"])
    f.close()
    # out= cv2.cv2.VideoWriter(file,cv2.cv2.VideoWriter_fourcc(*'MP4V'),ret["protocol"][0],(ret["protocol"][1],ret["protocol"][2]))
    # while (True):
    #     frame=socketDk.recv_pyobj()
    #     if frame["frame"] == "sucess":
    #         break
    #     out.write(frame["frame"])
