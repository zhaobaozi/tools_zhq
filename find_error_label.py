# -*- coding: utf-8 -*-  
import xml.dom.minidom  
import os  
import cv2
import shutil
path = "/home/zhaohuaqing/Downloads/cowa/COWA_dataset/traffic_light/traffic_lights/traffic_lights_normal/Annotations/"
save_dir="/home/zhaohuaqing/Downloads/cowa/COWA_dataset/traffic_light/delet/"
img_path="/home/zhaohuaqing/Downloads/cowa/COWA_dataset/traffic_light/traffic_light_1/"
files= os.listdir(path)
count=0
for file_name in files: 
    if file_name.endswith('xml'):  
        count=count+1
        #print "count:",count
        new_path1=path+file_name
        #print(path+file_name)
        DOMTree = xml.dom.minidom.parse(new_path1)  
        annotation = DOMTree.documentElement  
        filename = annotation.getElementsByTagName("filename")[0]  
        objects = annotation.getElementsByTagName("object")  


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
               count=count+1
            if name == "green":
               count=count+1
            if name == "yellow":
               count=count+1
            if name == "off":
               count=count+1
            if name != "red" and name != "green" and name != "yellow" and name != "off" :
                print "file_name:",file_name
     
       
