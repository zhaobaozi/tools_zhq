#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cv2
import os
import random
filename="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/output.txt"
image_root="/home/zhaohuaqing/Documents/baidu_images/"
image_new="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/images/"
labelpath='/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/labels/'
image_new_save="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/images1/"
labelpath_xml='/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/labels_xml/'
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



folder = os.path.exists(image_new)
if not folder:
   os.makedirs("/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/images/")
folder1 = os.path.exists(labelpath)
if not folder1:
    os.makedirs("/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/labels/")
folder2 = os.path.exists(image_new_save)
if not folder2:
   os.makedirs("/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/images1/")
folder3 = os.path.exists(labelpath_xml)
if not folder3:
   os.makedirs("/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip4/labels_xml/")
with open(filename, 'r') as file_to_read:
  while True:
    croproi = []
    images_name = {}
    images_name_xml={}
    labelxy = []
    lines = file_to_read.readline()
    if not lines:
      break
    lines=lines.rstrip("\n")
    str_list = lines.split(" ")
    image_name=str_list[0]
    img=cv2.imread(image_root+image_name)
    count=len(str_list)
    w=len(img[1])
    h=len(img)
    j=0
    name_num=0
    for i in range(1,count):
      img = cv2.imread(image_root + image_name)

      a=str_list[i].split(",")
      x1=int(a[0])
      y1=int(a[1])
      x2=int(a[2])
      y2=int(a[3])
      classname=a[4]
      if classname=='go' or classname=='goForward' or classname=='goLeft':
          classname='green'
      elif classname=='stop'or classname=='stopLeft':
          classname='red'
      elif classname == 'warning' or classname == 'WarningLeft':
          classname='yellow'
      if x1<0:x1=0
      if y1<0:y1=0
      if x2>w:x2=w
      if y2>h:y2=h

      x_center=int(x1+1/2*(x2-x1))
      y_center = int(y1 + 1 / 2 * (y2 - y1))
      rx = random.randint(-50, 50)
      ry = random.randint(-100, 100)
      x_center_new = x_center + rx
      y_center_new = y_center + ry
      randw = random.randint(200, 400)
      randh = random.randint(200, 400)
      x1_new = x_center_new - randw / 2
      y1_new = y_center_new - randh / 2
      x2_new = x_center_new + randw / 2
      y2_new = y_center_new + randh / 2
      if x1_new < 0: x1_new = 0
      if x1_new > w: x1_new = w
      if x2_new < 0: x2_new = 0
      if x2_new > w: x2_new = w
      if y2_new < 0: y2_new = 0
      if y2_new > h: y2_new = h
      if y1_new < 0: y1_new = 0
      if y1_new > h: x2_new = h
      rec1 = (x1_new, y1_new, x2_new, y2_new)
      rec2 = (x1, y1, x2, y2)
      IOU = compute_iou(rec1, rec2)
      if IOU > 0.6:
          j=j+1
          labelxy.append(x1)
          labelxy.append(y1)
          labelxy.append(x2)
          labelxy.append(y2)
          labelxy.append(classname)
          w_new = x2_new - x1_new
          h_new = y2_new - y1_new
          new_labeltxt = labelpath+image_name[:-4] + '-' + str(j) + '.txt'
          new_labeltxt_xml1=labelpath_xml+image_name[:-4] + '-' + str(j) + '.txt'
          name_num = name_num + 1
          images_name.update({name_num: new_labeltxt})
          images_name_xml.update({name_num: new_labeltxt_xml1})
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
          images_name_path1=image_new_save+image_name[:-4]+'-' + str(j)+'.jpg'
          cv2.imwrite(images_name_path1, imgcrop, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
          cv2.rectangle(imgcrop, (re_x1,re_y1), (re_x2, re_y2), (0, 255, 0), 1)
          images_name_path=image_new+image_name[:-4]+'-' + str(j)+'.jpg'
          cv2.imwrite(images_name_path ,imgcrop,[int(cv2.IMWRITE_JPEG_QUALITY),100])
          with open(new_labeltxt, 'a+') as f:
              str1 = classname + ' ' + str(re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
              f.write(str1)
          with open(new_labeltxt_xml1, 'a+') as f:
              str11 = image_name[:-4] + '-' + str(j) + '.jpg'+' '+classname + ' ' + str(re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
              f.write(str11)
      if j>=2:
          for r in range(1,j):
              rec2 = (x1, y1, x2, y2)
              rec1 = (croproi[(r - 1) * 4], croproi[(r - 1) * 4 + 1], croproi[(r - 1) * 4 + 2],
                      croproi[(r - 1) * 4 + 3])
              IOU = compute_iou(rec1, rec2)
              if IOU >= 0.6:
                  str3x1 = x1 - croproi[(r - 1) * 4]
                  str3y1 = y1 - croproi[(r - 1) * 4 + 1]
                  str3x2 = x2 - croproi[(r - 1) * 4]
                  str3y2 = y2 - croproi[(r - 1) * 4 + 1]
                  w_crop = croproi[(r - 1) * 4 + 2] - croproi[(r - 1) * 4]
                  h_crop = croproi[(r - 1) * 4 + 3] - croproi[(r - 1) * 4 + 1]

                  if str3x1 <= 0: str3x1 = 0
                  if str3y1 <= 0: str3y1 = 0
                  if str3x2 >= w_crop: str3x2 = w_crop
                  if str3y2 >= h_crop: str3y2 = h_crop
                  #re_imgcrop = img[croproi[(r - 1) * 4 + 1]:croproi[(r - 1) * 4 + 3],
                  #             croproi[(r - 1) * 4]:croproi[(r - 1) * 4 + 2]]

                  re_labeltxt = images_name[r]
                  re_labeltxt_xml=images_name_xml[r]
                  list3 = re_labeltxt.split('/')[-1]
                  re_image_path = image_new + list3[:-4]+ '.jpg'
                  re_imgcrop=cv2.imread(re_image_path)
                  cv2.rectangle(re_imgcrop, (str3x1, str3y1), (str3x2, str3y2), (0, 255, 0), 1)
                  str3 = classname+ ' ' + str(str3x1) + ' ' + str(str3y1) + ' ' + str(str3x2) + ' ' + str(str3y2) + '\n'
                  str33=list3[:-4]+ '.jpg'+' '+classname+ ' ' + str(str3x1) + ' ' + str(str3y1) + ' ' + str(str3x2) + ' ' + str(str3y2) + '\n'
                  cv2.imwrite(re_image_path, re_imgcrop)
                  with open(re_labeltxt, 'a+') as f:
                      f.write(str3)
                  with open(re_labeltxt_xml, 'a+') as f:
                      f.write(str33)
          for s in range(1, j):

              rec2 = (labelxy[(s - 1) * 5], labelxy[(s - 1) * 5 + 1], labelxy[(s - 1) * 5 + 2],
                      labelxy[(s - 1) * 5 + 3])
              rec1=(x1_new,y1_new,x2_new,y2_new)
              w_3=x2_new-x1_new
              h_3=y2_new-y1_new
              IOU = compute_iou(rec1, rec2)
              if IOU >= 0.6:
                  str2x1 = labelxy[(s - 1) * 5] - x1_new
                  str2y1 = labelxy[(s - 1) * 5 + 1] - y1_new
                  str2x2 = labelxy[(s - 1) * 5 + 2] - x1_new
                  str2y2 = labelxy[(s - 1) * 5 + 3] - y1_new
                  if str2x1 <= 0: str2x1 = 0
                  if str2y1 <= 0: str2y1 = 0
                  if str2x2 >= w_3: str2x2 = w_3
                  if str2y2 >= h_3: str2y2 = h_3
                  re_labeltxt1 = images_name[name_num]
                  re_labeltxt111=images_name_xml[name_num]
                  list2 = re_labeltxt1.split('/')[-1]
                  images_name3=image_new + list2[:-4]+ '.jpg'
                  imgcrop_3=cv2.imread(images_name3)

                  cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 1)
                  # cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 2)
                  cv2.imwrite(images_name3, imgcrop_3)
                  str2 = classname+ ' ' + str(str2x1) + ' ' + str(str2y1) + ' ' + str(str2x2) + ' ' + str(str2y2) + '\n'
                  str22 = list2[:-4]+ '.jpg'+' '+classname + ' ' + str(str2x1) + ' ' + str(str2y1) + ' ' + str(str2x2) + ' ' + str(str2y2) + '\n'
                  with open(re_labeltxt1, 'a+') as f:
                      f.write(str2)
                  with open(re_labeltxt111, 'a+') as f:
                      f.write(str22)
