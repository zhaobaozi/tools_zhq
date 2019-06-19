import yaml
import cv2
import numpy as np
import os
classname={0:'none',1:'off',2:'red',3:'yellow',4:'green',}
for i in range(0,5):
    print classname[i]
context_1=0.25
context_2=0.10
images = yaml.load(open('/home/zhaohuaqing/Downloads/tl_ssd/DTLD_Labels/Kassel_all.yml','rb').read())
image_new='/home/zhaohuaqing/Downloads/tl_ssd/normalimages_xml/'
root_path='/home/zhaohuaqing/Downloads/tl_ssd/'
labelpath='/home/zhaohuaqing/Downloads/tl_ssd/normallabels_xml/'
folder = os.path.exists(image_new)
if not folder:
    os.makedirs("/home/zhaohuaqing/Downloads/tl_ssd/normalimages_xml/")
folder1 = os.path.exists(labelpath)
if not folder1:
    os.makedirs("/home/zhaohuaqing/Downloads/tl_ssd/normallabels_xml/")
for i, image_dict in enumerate(images):
    imagepath=image_dict['path']
    #Essen[32:];Kassel[24:];Duesseldorf_all[24:];Bochum_all[24;]
    imagepath_new=root_path+imagepath[24:]
    img = cv2.imread(imagepath_new, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BAYER_GB2BGR)
    # Images are saved in 12 bit raw -> shift 4 bits
    img = np.right_shift(img, 4)
    img = img.astype(np.uint8)
    list1=imagepath_new.split('/')[-1]
    labeltxt=labelpath+list1[:-5]+'.txt'
    img_w=len(img[1])
    img_h=len(img)

    j=0
    for label in image_dict['objects']:
        classid=list(str(label['class_id']))
        if classid[0]==str(1) and classid[4]!=str(3) and classid[5]!=str(8) and classid[5]!=str(9):
            if label['width']*label['height']>200:
                x1=label['x']
                y1=label['y']
                x2=x1+label['width']
                y2=y1+label['height']
                if x1<0:x1=0
                if y1<0:y1=0
                if x2>img_w:
                    x2=img_w
                    print list1
                if y2>img_h:
                    y2=img_h
                    print list1
                w_new=x2-x1
                h_new=y2-y1
                x1_new=int(x1-context_1*w_new)
                y1_new=int(y1-context_2*h_new)
                x2_new=int(x2+context_1*w_new)
                y2_new=int(y2+context_2*h_new)
                if x1_new<0:x1_new=0
                if y1_new<0:y1_new=0
                if x2_new>img_w:
                    x2_new=img_w
                    print list1
                if y2_new>img_h:
                    y2_new=img_h
                #print int(class1)
                if classid[4] == str(4):
                    classid[4] = str(4)
                elif classid[4] == str(2):
                    classid[4] = str(3)
                elif classid[4] == str(1):
                    classid[4] = str(2)
                elif classid[4] == str(0):
                    classid[4] = str(1)
                str1=list1[:-5]+'.jpg'+' '+classname[int(classid[4])]+' '+str(x1_new)+' '+str(y1_new)+' '+str(x2_new)+' '+str(y2_new)+'\n'
                #str2=' '+str(classid)+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
                with open(labeltxt, 'a+') as f:
                    f.write(str1)
                    j = j + 1
                #cv2.rectangle(img, (x1_new, y1_new), (x2_new, y2_new), (0,255,0), 1)  # 15
    if j!=0:
        cv2.imwrite(image_new+list1[:-5] + '.jpg', img)

