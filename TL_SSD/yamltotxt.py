import yaml
import cv2
import numpy as np
import os
classname={0:'off',1:'red',2:'yellow',3:'green',4:'none'}
images = yaml.load(open('/home/zhaohuaqing/Downloads/tl_ssd/DTLD_Labels/Kassel_all.yml','rb').read())
image_new='/home/zhaohuaqing/Downloads/tl_ssd/images/'
root_path='/home/zhaohuaqing/Downloads/tl_ssd/'
labelpath='/home/zhaohuaqing/Downloads/tl_ssd/labels/'
for i, image_dict in enumerate(images):
    imagepath=image_dict['path']
    imagepath_new=root_path+imagepath[24:]
    img = cv2.imread(imagepath_new, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BAYER_GB2BGR)
    # Images are saved in 12 bit raw -> shift 4 bits
    img = np.right_shift(img, 4)
    img = img.astype(np.uint8)
    list1=imagepath_new.split('/')[-1]
    labeltxt=labelpath+list1[:-5]+'.txt'

    j=0
    for label in image_dict['objects']:
        classid=list(str(label['class_id']))
        if int(classid[0])==1 and int(classid[4]!=3) and int(classid[5])!=8 and int(classid[5])!=9:
            if label['width']*label['height']>200:
                x1=label['x']
                y1=label['y']
                x2=x1+label['width']
                y2=y1+label['height']
                class1=classid[4]
                #print int(class1)
                if int(class1)==4:
                    classid=3
                str1=list1[:-5]+'.jpg'+' '+str(classid)+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
                str2=' '+str(classid)+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
                with open(labeltxt, 'a+') as f:
                    if j!= 0:
                        f.write(str2)
                    else:
                        f.write(str1)
                    j = j + 1
                #cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)  # 15
    if j!=0:
        cv2.imwrite(image_new+list1[:-5] + '.jpg', img)

