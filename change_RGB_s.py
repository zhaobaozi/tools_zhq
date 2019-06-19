# coding=utf-8
import numpy as np
import cv2 as cv
 
img = cv.imread("/home/zhaohuaqing/Documents/image2/1544773817.527648.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
winName = "image"
cv.namedWindow(winName)
 
switch = '0 : OFF \n1 : ON'
 
def nothing(x):
    r = cv.getTrackbarPos('R', winName)
    g = cv.getTrackbarPos('G', winName)
    b = cv.getTrackbarPos('B', winName)
    s = cv.getTrackbarPos(switch, winName)
    if s == 0:
        img = 0
    else:
        img = cv.imread("/home/zhaohuaqing/Documents/image2/1544773817.527648.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
        img=img[:]
        if b!=128:
            img[:,:,0]=img[:,:,0]*(b/128.0)
            
        if g!=128:
            img[:,:,1]=img[:,:,1]*(g/128.0)
      
        if r!=128:
            img[:,:,2]=img[:,:,2]*(r/128.0)
        print "B:",b/128.0,"G:",g/128.0,"R:",r/128.0
        print "********************"
    
    cv.imshow('image', img)
 
 
if __name__ == '__main__':
    cv.imshow('image',img)
    cv.createTrackbar('R', winName, 128, 255, nothing)
    cv.createTrackbar('G', winName, 128, 255, nothing)
    cv.createTrackbar('B', winName, 128, 255, nothing)
    cv.createTrackbar(switch, winName, 0, 1, nothing)

    cv.waitKey(0)
    cv.destroyAllWindows()

