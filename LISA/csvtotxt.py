#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
import cv2

dict = {'go': '1', 'goForward': '2', 'goLeft': '3', 'stop': '4', 'stopLeft': '5', 'warning': '6','WarningLeft': '7', 'non_of_above': '8'}

def read_csv(imput_file, out__path):
	csv = open(os.path.abspath(imput_file), 'r')
	csv.readline() # Discard the header-line.
	lines = csv.readlines()
	file_output = open(out__path+'/output.txt', 'w')
	image_name2 = ''
	#del lines[856:880]
	i=0
	for line in lines:
		Comp = line.split(';')
		Comp2 = Comp[0].split('/')	
		image_name = Comp2[1]
		w=int(Comp[4])-int(Comp[2])
		h=int(Comp[5])-int(Comp[3])
		xcenter=int(Comp[2])+w/2
		ycenter = int(Comp[3]) + h / 2
		w_1=2.5*w
		h_1=2.5*h
		if w_1>h_1:
			pad=w_1
		else:
			pad=h_1
		x1=int(xcenter-pad/2)
		y1=int(ycenter-pad/2)
		x2=int(xcenter+pad/2)
		y2=int(ycenter+pad/2)
		image_path=output_folder+'frames/'+image_name
		new_output_folder=output_folder+'newframes/'
		if not os.path.exists(new_output_folder):
			os.mkdir(new_output_folder)

		new_image_path=new_output_folder+image_name
		img = cv2.imread(image_path)
		orig_img_width=len(img[0])
		orig_img_height=len(img)
		if x1 <= 0: x1 = 0
		if x2 >= orig_img_width: x2 = orig_img_width
		if y1 <= 0: y1 = 0
		if y2 >= orig_img_height: y2 = orig_img_height

		cut = img[y1:y2, x1:x2]
		labelx1=int(Comp[2])-x1
		labelx2=int(Comp[4])-x1
		labely1 = int(Comp[3]) - y1
		labely2 = int(Comp[5]) - y1
		#cv2.rectangle(img, (x1,y1), (x2,y2), (0, 255, 0), 3)
		cv2.rectangle(cut, (labelx1, labely1), (labelx2, labely2), (0, 255, 0), 3)
		if os.path.exists(new_image_path):
			new_image_path=new_image_path[:-4]+'-'+str(i)+'.png'
			new_image_name=image_name[:-4]+str(i)+'.png'
		else:
			new_image_name=image_name
		cv2.imwrite(new_image_path, cut)
		#cv2.namedWindow("resultpicture")
		#cv2.imshow("resultpicture", cut)
		#cv2.waitKey(0)
		i=i+1
		x22=float(h)/float(w)
		labelx2 = int(Comp[4]) - x1
		if h>w:
			boxclass=1
			if 0.9<x22<1.1:
				boxclass=3
		elif h<w:
			boxclass=2
			if 0.9<x22<1.1:
				boxclass=3
		elif h==w:
			boxclass=3
		print(image_name)
		xcenter=int(Comp[2])+w/2
		ycenter=int(Comp[3])+w/2
		if image_name == image_name2:
			file_output.write(' ' + ','+str(labelx1)+','+str(labely1)+','+str(labelx2)+','+str(labely2)+ ',' + str(boxclass))


		else:
			file_output.write('\n' + new_image_name + ' ' + str(labelx1)+','+str(labely1)+','+str(labelx2)+','+str(labely2) + ',' + str(boxclass))

	file_output.close()
	csv.close()

def labeled_sample(image_txt_full_path, save_txt_path):
	fr = open(image_txt_full_path,'r')
	min_est = 30
	images = fr.readlines()
	cnt = 0
	for tmp, image in enumerate(images):
		inx = image.find('.png')
		if inx != -1 :
			image_name = image[:inx]
			image_num = image_name[12:17]
			if cnt != int(image_num):
				diff = int(image_num)-cnt
				cnt = int(image_num)
				print(image_num + ' ' + str(diff))
				cnt += 1
			else:
				cnt += 1
			inx = inx+4
			corrids = image[inx:].strip('\n')
			corrids = corrids.strip()
			corrids = corrids.split(' ')
			target_num = len(corrids)
			write_full_path = save_txt_path + image_name + '.txt'
			wr_context = ''
			for i, corrid in enumerate(corrids):
				corrid = corrid.replace(',', ' ')
				test_cor = corrid.split(' ')
				zz = test_cor[0] + ' ' + test_cor[1] + ' ' + test_cor[2] + ' ' + test_cor[3]
				zz_c = test_cor[4]
				wr_context = wr_context + zz_c + ' ' + zz + '\n'
			if target_num > 0:

				fw = open(write_full_path,'w')
				fw.write(wr_context)
				fw.close()
	fr.close()

if __name__ == '__main__':
	label_file ='/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip2/frameAnnotationsBOX.csv'
	output_folder = '/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip2/'
	read_csv(label_file, output_folder)
	image_txt_full_path = output_folder + 'output.txt'
	save_txt_path = output_folder + 'Labels/'
	if not os.path.exists(save_txt_path):
		os.mkdir(save_txt_path)
	labeled_sample(image_txt_full_path, save_txt_path)
	path1=output_folder+'/newframes/'
	path2 =output_folder+'/Labels/'
