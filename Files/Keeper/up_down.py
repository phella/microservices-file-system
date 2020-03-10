import zmq
import sys
import random
import time
import os
import cv2 

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
    f = open(file,'rb')
    rd = f.read()
    socketDk.send_pyobj({"type":"upload","file" : rd ,"filename" : file})
    f.close()
    return socketDk.recv_pyobj()


def download (socketDk,file ,filename):
    # socketDk.send_pyobj({"type" : "download" , "file":file })
    f = open(filename , 'wb')
    f.write(file)
    f.close()
    socketDk.send_string("succeful uploading")
    # out= cv2.cv2.VideoWriter(file,cv2.cv2.VideoWriter_fourcc(*'MP4V'),ret["protocol"][0],(ret["protocol"][1],ret["protocol"][2]))
    # while (True):
    #     frame=socketDk.recv_pyobj()
    #     if frame["frame"] == "sucess":
    #         break
    #     out.write(frame["frame"])
