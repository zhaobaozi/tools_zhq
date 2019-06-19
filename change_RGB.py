# coding=utf-8
import numpy as np
import cv2 as cv
 
img = cv.imread("/home/zhaohuaqing/Documents/image2/1544773817.527648.jpg",cv.IMREAD_COLOR)
winName = "image"
cv.namedWindow(winName)
 
def nothing(x):
    r = cv.getTrackbarPos('R', winName)
    g = cv.getTrackbarPos('G', winName)
    b = cv.getTrackbarPos('B', winName)
  
    img = cv.imread("/home/zhaohuaqing/Documents/image2/1544773817.527648.jpg",cv.IMREAD_COLOR)
    img=img[:]
    img[:,:,0]=img[:,:,0]*(b/128.0)    
    img[:,:,1]=img[:,:,1]*(g/128.0)
    img[:,:,2]=img[:,:,2]*(r/128.0)
    print "B:",b/128.0,"G:",g/128.0,"R:",r/128.0
    print "********************"
    cv.imshow('image', img)
 
 
if __name__ == '__main__':
    cv.imshow('image',img)
    cv.createTrackbar('R', winName, 128, 255, nothing)
    cv.createTrackbar('G', winName, 128, 255, nothing)
    cv.createTrackbar('B', winName, 128, 255, nothing)

    cv.waitKey(0)
    cv.destroyAllWindows()

