# coding=utf-8
import numpy as np
import cv2 as cv
 
img = cv.imread("/home/zhaohuaqing/Pictures/Screenshot from 2019-04-01 16-13-19.png",cv.IMREAD_COLOR)
winName = "image"
cv.namedWindow(winName)
 
def nothing(x):
    a = cv.getTrackbarPos('a', winName)
    b = cv.getTrackbarPos('b', winName)
   
  
    img = cv.imread("/home/zhaohuaqing/Pictures/Screenshot from 2019-04-01 16-13-19.png",cv.IMREAD_COLOR)
    rows,cols,channels=img.shape
    blank = np.zeros([rows, cols, channels], img.dtype)
    img = cv.addWeighted(img, a/100.0, blank, 1-a, b)
    cv.imshow('image',img)
 
    print "a:",a/100.0,"b:",b
    print "********************"
 
 
if __name__ == '__main__':
    cv.imshow('image',img)
    cv.createTrackbar('a', winName, 0, 300, nothing)
    cv.createTrackbar('b', winName, 0, 200, nothing)


    cv.waitKey(0)
    cv.destroyAllWindows()

