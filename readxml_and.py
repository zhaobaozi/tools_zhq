# -*- coding: utf-8 -*-  
import xml.dom.minidom  
import os  
import cv2
import shutil
path = "/home/zhaohuaqing/zhq/Data-Augment/Annotations/"
save_dir="/home/zhaohuaqing/zhq/Data-Augment/JPEGImages/"
img_path="/home/zhaohuaqing/zhq/Data-Augment/JPEGImages/"
files= os.listdir(path)
count=0
for file_name in files: 
    if file_name.endswith('xml'):  
        count=count+1
        print "count:",count
        new_path1=path+file_name
        print(path+file_name)
        DOMTree = xml.dom.minidom.parse(new_path1)  
        annotation = DOMTree.documentElement  
        filename = annotation.getElementsByTagName("filename")[0]  
        imgname = filename.childNodes[0].data 
        objects = annotation.getElementsByTagName("object")  
        img=cv2.imread(img_path+imgname)

        for object in objects:  

            bbox = object.getElementsByTagName("bndbox")[0]
            name = object.getElementsByTagName("name")[0]  
            name = name.childNodes[0].data 
            xmin = bbox.getElementsByTagName("xmin")[0]  
            xmin = xmin.childNodes[0].data  
            ymin = bbox.getElementsByTagName("ymin")[0]  
            ymin = ymin.childNodes[0].data   
            xmax = bbox.getElementsByTagName("xmax")[0]  
            xmax = xmax.childNodes[0].data   
            ymax = bbox.getElementsByTagName("ymax")[0] 
            ymax = ymax.childNodes[0].data  
            if name == "red":
                cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,0,255),1)
            if name == "green":
                cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,0),1)
            if name == "yellow":
                cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,255),1)
            if name == "off":
                cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,255,255),1)
        cv2.imshow('image', img)
        k = cv2.waitKey(0)& 0xFF
        if k == ord('s'): # wait for 's' key to save and exit
            shutil.move(img_path+imgname,save_dir+imgname)
            shutil.move(path+file_name,save_dir+file_name)
            print "save relabel..."
        elif k == ord('w'): # wait for 's' key to save and exit
            continue

       
