# -*- coding: utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--point_txt', type=str, required=True,
		            help='save_point')
	parser.add_argument('--img_path', type=str, required=True,
		            help='read img to process')
	parser.add_argument('--median_threshold', type=int, required=True,
		            help='You can adjust it yourself')
	parser.add_argument('--mask_threshold', type=int, required=True,
		            help='You can adjust it yourself')
	parser.add_argument('--median_kernel', type=int, required=True,
		            help='You can adjust it yourself')
	args = parser.parse_args()
	img = cv2.imread(args.img_path,0)#原图
	kernel = np.ones((11,11),np.uint8)
	kernel2 = np.ones((3,3),np.uint8)
	img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel2)#闭运算填补空洞小点
	img_median = cv2.medianBlur(img_close, args.median_kernel)#中值滤波
	cv2.imwrite("./result/img_median.jpg",img_median)

	x = cv2.Sobel(img_median,cv2.CV_16S,1,0)#scharr求梯度提取梯度线
	y = cv2.Sobel(img_median,cv2.CV_16S,0,1)
	absX = cv2.convertScaleAbs(x)  
	absY = cv2.convertScaleAbs(y)
	img_scharr = cv2.addWeighted(absX,0.5,absY,0.5,0)
	cv2.imwrite("./result/img_scharr.jpg",img_scharr)

	img_median[img_median>=args.median_threshold]=255##腐蚀中值滤波图，作为mask模板以备消除边界梯度，先根据一定阈值转化为二值图
	img_median[img_median<=args.median_threshold]=0
	img_erosion = cv2.erode(img_median,kernel,iterations = 1)
	cv2.imwrite("./result/img_erosion.jpg",img_erosion)

	img_mask = cv2.bitwise_and(img_scharr, img_scharr, mask=img_erosion)#除边界梯度，并设置阈值转化为二值图
	img_mask[img_mask>args.mask_threshold]=255
	img_mask[img_mask<args.mask_threshold]=0
	cv2.imwrite("./result/result.jpg",img_mask)
	print "img haved been saved in result"
	height = img_mask.shape[0]#存储梯度线坐标
	weight =img_mask.shape[1]
	with open(args.point_txt, 'a+') as f:
		for row in range(height):      
			for col in range(weight): 
				if img_mask[row][col]==255:
					str1 = str(row) + ' ' + str(col) + '\n'
					f.write(str1)
	print "txt haved been saved in result"


