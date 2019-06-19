# -*- coding: utf-8 -*-  
import xml.dom.minidom  
import os  
import cv2
import random
image_root="/home/zhaohuaqing/Documents/4_2/JPEGImages/"
image_new="/home/zhaohuaqing/Documents/4_2/images2/"
labelpath='/home/zhaohuaqing/Documents/4_2/labels2/'
image_new_save="/home/zhaohuaqing/Documents/4_2/images1/"
labelpath_xml='/home/zhaohuaqing/Documents/4_2/labels1/'
path = "/home/zhaohuaqing/Documents/4_2/Annotations/"
files= os.listdir(path)
a=0
b=0
croproi = []
images_name = {}
images_name_xml={}
labelxy = []

folder = os.path.exists(image_new)
if not folder:
   os.makedirs("/home/zhaohuaqing/Documents/4_2/images2/")
folder1 = os.path.exists(labelpath)
if not folder1:
    os.makedirs("/home/zhaohuaqing/Documents/4_2/labels2/")
folder2 = os.path.exists(image_new_save)
if not folder2:
   os.makedirs("/home/zhaohuaqing/Documents/4_2/images1/")
folder3 = os.path.exists(labelpath_xml)
if not folder3:
   os.makedirs("/home/zhaohuaqing/Documents/4_2/labels1/")
def compute_iou(rec1, rec2):

	S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
	S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

	left_line = max(rec1[1], rec2[1])
	right_line = min(rec1[3], rec2[3])
	top_line = max(rec1[0], rec2[0])
	bottom_line = min(rec1[2], rec2[2])

	if left_line >= right_line or top_line >= bottom_line:
		return 0
	else:
		intersect = float((right_line - left_line) * (bottom_line - top_line))
                print intersect / S_rec2
		return intersect / S_rec2
         
for file_name in files: 
	if file_name.endswith('xml'):
		croproi = []
		images_name = {}
		images_name_xml = {}
		labelxy = []
		j=0
		name_num=0
		new_path1=path+file_name
		print(path+file_name)
		DOMTree = xml.dom.minidom.parse(new_path1)  
		annotation = DOMTree.documentElement  
		filename = annotation.getElementsByTagName("filename")[0]  
		imgname = filename.childNodes[0].data 
		objects = annotation.getElementsByTagName("object")
		len1=len(objects)
		for i in xrange(len1):
			object=objects[i]
			img = cv2.imread(image_root + imgname)
			bbox = object.getElementsByTagName("bndbox")[0]
			name = object.getElementsByTagName("name")[0]  
			name = name.childNodes[0].data
			classname=name
			x1 = bbox.getElementsByTagName("xmin")[0]
			x1 = int(x1.childNodes[0].data)
			y1 = bbox.getElementsByTagName("ymin")[0]
			y1 = int(y1.childNodes[0].data)
			x2 = bbox.getElementsByTagName("xmax")[0]
			x2 = int(x2.childNodes[0].data)
			y2 = bbox.getElementsByTagName("ymax")[0]
			y2 = int(y2.childNodes[0].data)
			w=len(img[1])
			h=len(img)
			xwight=int(x2)-int(x1)
			yheight=int(y2)-int(y1)
			if x1<=0:x1=0
			if y1<=0:y1=0
			if x2>=w:x2=w
			if y2>=h:y2=h
			x_11=int(0.5*xwight)
			y_11=int(0.5*yheight)
			x_center=x1+x_11
			y_center = y1 + y_11
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
				  new_labeltxt = labelpath+imgname[:-4] + '-' + str(j) + '.txt'
				  new_labeltxt_xml1=labelpath_xml+imgname[:-4] + '-' + str(j) + '.txt'
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
				  images_name_path1=image_new_save+imgname[:-4]+'-' + str(j)+'.jpg'
				  cv2.imwrite(images_name_path1, imgcrop, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
				  cv2.rectangle(imgcrop, (re_x1,re_y1), (re_x2, re_y2), (0, 255, 0), 1)
                                  cv2.putText(imgcrop, classname, (re_x1, re_y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                       thickness=2)
				  images_name_path=image_new+imgname[:-4]+'-' + str(j)+'.jpg'
				  cv2.imwrite(images_name_path ,imgcrop,[int(cv2.IMWRITE_JPEG_QUALITY),100])
				  with open(new_labeltxt, 'a+') as f:
				      str1 = classname + ' ' + str(re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
				      f.write(str1)
				  with open(new_labeltxt_xml1, 'a+') as f:
				      str11 = imgname[:-4] + '-' + str(j) + '.jpg'+' '+classname + ' ' + str(re_x1) + ' ' + str(re_y1) + ' ' + str(re_x2) + ' ' + str(re_y2) + '\n'
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

						re_labeltxt = images_name[r]
						re_labeltxt_xml=images_name_xml[r]
						list3 = re_labeltxt.split('/')[-1]
						re_image_path = image_new + list3[:-4]+ '.jpg'
						re_imgcrop=cv2.imread(re_image_path)
						cv2.rectangle(re_imgcrop, (str3x1, str3y1), (str3x2, str3y2), (0, 255, 0), 1)
                                                cv2.putText(re_imgcrop, classname, (str3x1, str3y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                       thickness=2)
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
                                                cv2.putText(imgcrop_3, labelxy[(s - 1) * 5 + 4], (str2x1, str2y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                       thickness=2)
						cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 1)
                                               
		          # cv2.rectangle(imgcrop_3, (str2x1, str2y1), (str2x2, str2y2), (0, 255, 0), 2)
						cv2.imwrite(images_name3, imgcrop_3)
						str2 = labelxy[(s - 1) * 5 + 4]+ ' ' + str(str2x1) + ' ' + str(str2y1) + ' ' + str(str2x2) + ' ' + str(str2y2) + '\n'
						str22 = list2[:-4]+ '.jpg'+' '+labelxy[(s - 1) * 5 + 4] + ' ' + str(str2x1) + ' ' + str(str2y1) + ' ' + str(str2x2) + ' ' + str(str2y2) + '\n'
						with open(re_labeltxt1, 'a+') as f:
							f.write(str2)
						with open(re_labeltxt111, 'a+') as f:
							f.write(str22)
