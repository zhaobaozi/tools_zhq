import yaml
import cv2
import numpy as np
import random
import os
classname={0:'none',1:'off',2:'red',3:'yellow',4:'green',}
for i in range(0,5):
    print classname[i]
#Bochum24,kassel24,essen32,buess24,dortmund24,fulda24,bremen24/Hannover24/berlin24
images = yaml.load(open('/home/zhaohuaqing/Downloads/tl_ssd/DTLD_Labels/Bremen_all.yml','rb').read())
image_new='/home/zhaohuaqing/Downloads/tl_ssd/bremen_small/'
#image_new='/home/zhaohuaqing/Downloads/tl_ssd/images8/'
root_path='/home/zhaohuaqing/Downloads/tl_ssd/'
labelpath='/home/zhaohuaqing/Downloads/tl_ssd/bremen_label/'
#labelpath='/home/zhaohuaqing/Downloads/tl_ssd/labels8/'


def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area


    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return intersect / S_rec2



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
    w=len(img[1])
    h=len(img)
    j=0
    labelxy=[]
    croproi=[]
    name_num=0
    count_list=[]
    images_name={}
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
                if x2>w:
                    x2=w
                    print list1
                if y2>h:
                    y2=h
                    print list1
                x_center=x1+label['width']/2
                y_center=y1+label['height']/2
                j = j + 1
                if classid[4] == str(4):
                    classid[4] = str(4)
                elif classid[4] == str(2):
                    classid[4] = str(3)
                elif classid[4] == str(1):
                    classid[4] = str(2)
                elif classid[4] == str(0):
                    classid[4] = str(1)
                labelxy.append(x1)
                labelxy.append(y1)
                labelxy.append(x2)
                labelxy.append(y2)
                labelxy.append(classid[4])
                count=0
                if x1 == 0 or y1 == 0 or x2 == w or y2 == h:
                    count=count+1
                    rx=random.randint(-label['width'],label['width'])
                    ry=random.randint(-label['height'],label['height'])
                    x_center_new=x_center+rx
                    y_center_new=y_center+ry
                    randw1 = random.randint(200, 400)
                    randh1 = random.randint(200, 400)
                    x1_new=x_center_new-randw1/2
                    y1_new=y_center_new-randh1/2
                    x2_new=x_center_new+randw1/2
                    y2_new=y_center_new+randh1/2
                    if x1_new < 0: x1_new = 0
                    if x1_new > w: x1_new = w
                    if x2_new < 0: x2_new = 0
                    if x2_new > w: x2_new = w
                    if y2_new < 0: y2_new = 0
                    if y2_new > h: y2_new = h
                    if y1_new < 0: y1_new = 0
                    if y1_new > h: x2_new = h
                    w_new = x2_new - x1_new
                    h_new = y2_new - y1_new

                    new_labeltxt = labelpath + list1[:-5] + '-' + str(j) + '-'+str(count)+''+'.txt'
                    name_num=name_num+1
                    images_name.update({name_num: new_labeltxt})
                    croproi.append(x1_new)
                    croproi.append(y1_new)
                    croproi.append(x2_new)
                    croproi.append(y2_new)
                    re_x1 = x1 - x1_new
                    if re_x1 <= 0: re_x1 = 0
                    re_x2 = x2 - x1_new
                    if re_x2 >= w_new: re_x2 = w_new
                    re_y1 = y1 - y1_new
                    if re_y1 <= 0: re_y1 = 0
                    re_y2 = y2 - y1_new
                    if re_y2 >= h_new: re_y2 = h_new
                    imgcrop = img[y1_new:y2_new, x1_new:x2_new]
                    if re_x2 <= re_x1: print(list1)
                    if re_y2 <= re_y1: print(list1)
                    #cv2.rectangle(imgcrop, (re_x1,re_y1), (re_x2, re_y2), (0, 255, 0), 1)
                    cv2.imwrite(image_new + list1[:-5] + '-' + str(j) +'-'+str(count)+'.jpg', imgcrop)
                    with open(new_labeltxt, 'a+') as f:
                        str1 = list1[:-5] + '-' + str(j) +'-'+ str(count)+'.jpg' + ' ' + classname[int(classid[4])] + ' ' + str(
                            re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
                        f.write(str1)
                else:
                    count_d=random.randint(1,2)
                    while(count<count_d):
                            rx = random.randint(-50,50)
                            ry = random.randint(-100,100)
                            x_center_new = x_center + rx
                            y_center_new = y_center + ry
                            randw=random.randint(200,400)
                            randh=random.randint(200,400)
                            x1_new = x_center_new - randw/2
                            y1_new = y_center_new - randh/2
                            x2_new = x_center_new + randw/2
                            y2_new = y_center_new + randh/2
                            if x1_new < 0: x1_new = 0
                            if x1_new > w: x1_new = w
                            if x2_new < 0: x2_new = 0
                            if x2_new > w: x2_new = w
                            if y2_new < 0: y2_new = 0
                            if y2_new > h: y2_new = h
                            if y1_new < 0: y1_new = 0
                            if y1_new > h: x2_new = h
                            rec1=(x1_new,y1_new,x2_new,y2_new)
                            rec2=(x1,y1,x2,y2)
                            IOU = compute_iou(rec1, rec2)
                            if IOU>0.8:
                                count=count+1
                                w_new = x2_new - x1_new
                                h_new = y2_new - y1_new
                                new_labeltxt = labelpath + list1[:-5] + '-' + str(j) +'-'+str(count)+'.txt'
                                name_num = name_num + 1
                                images_name.update({name_num: new_labeltxt})


                                croproi.append(x1_new)
                                croproi.append(y1_new)
                                croproi.append(x2_new)
                                croproi.append(y2_new)
                                re_x1 = x1 - x1_new
                                if re_x1 <= 0: re_x1 = 0
                                re_x2 = x2 - x1_new
                                if re_x2 >= w_new: re_x2 = w_new
                                re_y1 = y1 - y1_new
                                if re_y1 <= 0: re_y1 = 0
                                re_y2 = y2 - y1_new
                                if re_y2 >= h_new: re_y2 = h_new
                                imgcrop_2 = img[y1_new:y2_new, x1_new:x2_new]
                                if re_x2 <= re_x1: print(list1)
                                if re_y2 <= re_y1: print(list1)
                                #cv2.rectangle(imgcrop_2, (re_x1,re_y1), (re_x2, re_y2), (0, 255, 0), 1)
                                cv2.imwrite(image_new + list1[:-5] + '-' + str(j) +'-'+str(count)+ '.jpg', imgcrop_2)
                                with open(new_labeltxt, 'a+') as f:
                                    str1 = list1[:-5] + '-' + str(j) + '-'+str(count)+'.jpg' + ' ' + classname[int(classid[4])] + ' ' + str(re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
                                    f.write(str1)
                count_list.append(count)
                if j>=2:
                    sumcount=0
                    sumcount_0=0
                    sumcount_cha=0


                    if j==2:sumcount_0=count_list[0]
                    else:
                        for o in range(0,j-1):
                            sumcount_0=sumcount_0+count_list[o]
                    for c in range(1,sumcount_0+1):
                        rec2 = (x1, y1, x2, y2)
                        rec1 = (croproi[(c - 1) * 4], croproi[(c - 1) * 4 + 1], croproi[(c - 1) * 4 + 2],
                                croproi[(c - 1) * 4 + 3])
                        IOU = compute_iou(rec1, rec2)
                        if IOU >= 0.7:
                            str3x1 = x1 - croproi[(c - 1) * 4]
                            str3y1 = y1 - croproi[(c - 1) * 4 + 1]
                            str3x2 = x2 - croproi[(c - 1) * 4]
                            str3y2 = y2 - croproi[(c - 1) * 4 + 1]
                            w_crop = croproi[(c - 1) * 4 + 2] - croproi[(c - 1) * 4]
                            h_crop = croproi[(c - 1) * 4 + 3] - croproi[(c - 1) * 4 + 1]

                            if str3x1 <= 0: str3x1 = 0
                            if str3y1 <= 0: str3y1 = 0
                            if str3x2 >= w_crop: str3x2 = w_crop
                            if str3y2 >= h_crop: str3y2 = h_crop
                            re_imgcrop = img[croproi[(c - 1) * 4 + 1]:croproi[(c - 1) * 4 + 3],
                                         croproi[(c - 1) * 4]:croproi[(c - 1) * 4 + 2]]
                            #cv2.rectangle(re_imgcrop, (str3x1, str3y1), (str3x2, str3y2), (0, 255, 0), 1)
                            re_labeltxt = images_name[c]
                            list3 = re_labeltxt.split('/')[-1]
                            if str3x2 <= str3x1: print(list3)
                            if str3y2 <= str3y1: print(list3)
                            str3 = list3[:-4] + '.jpg' + ' ' + classname[int(classid[4])] + ' ' + str(str3x1) + ' ' + str(str3y1) + ' ' + str(str3x2) + ' ' + str(str3y2) + '\n'
                            re_image_path = image_new + list3[:-4] + '.jpg'
                            cv2.imwrite(re_image_path, re_imgcrop)
                            with open(re_labeltxt, 'a+') as f:
                                f.write(str3)

                    for t in range(sumcount_0+1,sumcount_0+count_list[j-1]+1):
                        rec1 = (croproi[(t-1)*4], croproi[(t-1)*4+1], croproi[(t-1)*4+2], croproi[(t-1)*4+3])
                        w_3=croproi[(t-1)*4+2]-croproi[(t-1)*4]
                        h_3=croproi[(t-1)*4+3]-croproi[(t-1)*4+1]
                        for s in range(1,j):

                            rec2 = (labelxy[(s - 1) * 5], labelxy[(s - 1) * 5 + 1], labelxy[(s - 1) * 5 + 2],
                                    labelxy[(s - 1) * 5 + 3])
                            IOU = compute_iou(rec1, rec2)
                            if IOU >= 0.7:
                                str2x1 = labelxy[(s - 1) * 5 ]- croproi[(t-1)*4]
                                str2y1 = labelxy[(s - 1) * 5 + 1] - croproi[(t-1)*4+1]
                                str2x2 = labelxy[(s - 1) * 5 + 2] - croproi[(t-1)*4]
                                str2y2 = labelxy[(s - 1) * 5 + 3] - croproi[(t-1)*4+1]
                                if str2x1 <= 0: str2x1 = 0
                                if str2y1 <= 0: str2y1 = 0
                                if str2x2 >= w_3: str2x2 = w_3
                                if str2y2 >= h_3: str2y2 = h_3
                                re_labeltxt1=images_name[t]
                                list2 = re_labeltxt1.split('/')[-1]
                                imgcrop_3 = img[croproi[(t-1)*4+1]:croproi[(t-1)*4+3], croproi[(t-1)*4]:croproi[(t-1)*4+2]]
                                #cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 2)
                                #cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 2)
                                cv2.imwrite(image_new + list2[:-4]+'.jpg', imgcrop_3)
                                str2 = list2[:-4] + '.jpg' + ' ' + classname[int(labelxy[(s - 1) * 5 + 4])] + ' ' + str(str2x1) + ' ' + str(str2y1) + ' ' + str(str2x2) + ' ' + str(str2y2) + '\n'
                                with open(re_labeltxt1, 'a+') as f:
                                    f.write(str2)








