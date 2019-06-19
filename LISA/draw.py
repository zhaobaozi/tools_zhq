#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cv2
import os
filename="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip3/output.txt"
image_root="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip3/frames/"
image_new="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip3/images/"
folder = os.path.exists(image_new)
if not folder:
   os.makedirs("/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip3/images/")
with open(filename, 'r') as file_to_read:
  while True:
    lines = file_to_read.readline() # 整行读取数
    if not lines:
      break
    lines=lines.rstrip("\n")
    str_list = lines.split(" ")
    image_name=str_list[0]
    img=cv2.imread(image_root+image_name)
    count=len(str_list)
    for i in range(1,count):
      a=str_list[i].split(",")
      xmin=a[0]
      ymin=a[1]
      xmax=a[2]
      ymax=a[3]
      classname=a[4]
      cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,0),1)
      cv2.putText(img, str(classname), (int(xmin),int(ymin)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv2.imwrite(image_new+image_name[:-3]+'jpg',img,[int(cv2.IMWRITE_JPEG_QUALITY),100])

