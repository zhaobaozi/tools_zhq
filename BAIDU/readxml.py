# -*- coding: utf-8 -*-  
import xml.dom.minidom  
import os  
import cv2
path = "/home/zhaohuaqing/Documents/baidu/baidu_labels/"
files= os.listdir(path)
txt ='/home/zhaohuaqing/Documents/baidu/normaltxt/'
images_path="/home/zhaohuaqing/Documents/baidu/baidu_images/"
new_images_path="/home/zhaohuaqing/Documents/baidu/normalimages/"
a=0
b=0
#new_path="/home/zhaohuaqing/Downloads/tl_ssd/VOC2007/images/"
for file_name in files: 
    if file_name.endswith('xml'):  
        
        new_path1=path+file_name
        print(path+file_name)
        DOMTree = xml.dom.minidom.parse(new_path1)  
        annotation = DOMTree.documentElement  
        filename = annotation.getElementsByTagName("filename")[0]  
        imgname = filename.childNodes[0].data 
        objects = annotation.getElementsByTagName("object")  
        img=cv2.imread(images_path+imgname)
        new_labeltxt=txt+imgname[:-4]+'.txt'
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
            w=len(img[1])
            h=len(img)
            xwight=int(xmax)-int(xmin)
            yheight=int(ymax)-int(ymin)
            new_xmin=int(xmin)-int(a*xwight)
            new_ymin=int(ymin)-int(b*yheight)
            new_xmax=int(xmax)+int(a*xwight)
            new_ymax=int(ymax)+int(b*yheight)
            if new_xmin<=0:new_xmin=0
            if new_ymin<=0:new_ymin=0
            if new_xmax>=w:new_xmax=w
            if new_ymax>=h:new_ymax=h      
            #img=cv2.imread("/home/zhaohuaqing/Downloads/tl_ssd/VOC2007/JPEGImages/"+imgname)
            #cv2.rectangle(img,(int(new_xmin),int(new_ymin)),(int(new_xmax),int(new_ymax)),(0,0,255),3)
            
            with open(new_labeltxt, 'a+') as f:
                str1=str(name)+' '+str(new_xmin)+' '+str(new_ymin)+' '+str(new_xmax)+' '+str(new_ymax)+'\n'
                f.write(str1)
        cv2.imwrite(new_images_path+imgname,img)

       
