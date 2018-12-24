import cv2
import numpy as np
import time
import sys

def getSolidColor(b,g,r,h,w,d):
    img = np.zeros([h, w, d], np.uint8)
    img[:, :, 0] = np.ones([h, w])* b
    img[:, :, 1] = np.ones([h, w])* g
    img[:, :, 2] = np.ones([h, w])* r
    return img

def createIMG():
    solid = getSolidColor(0,255,0,360,640,3)
    cv2.circle(solid, (447, 63), 63, (0, 0, 255), -1)
    text = sys.argv[1]
    name = r"C:\Users\ws\Downloads\%s_%f.png"%(text,time.time())
    print(name)
    cv2.imwrite(name,solid)
    # cv2.imshow('',solid)
    # cv2.waitKey(0)

if __name__ == '__main__':
    createIMG()