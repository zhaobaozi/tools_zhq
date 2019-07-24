#!/bin/bash
POINT_TXT=./result/point.txt #输入马路牙子二维坐标
IMG_PATH=./result/2d_img.jpg #输入点云投影的二维图
MEDIAN_THRESHOLD=100 #可调阈值，中值化后以这个值作为阈值二值化图像
MASK_THRESHOLD=120 #可调阈值，对MASK后以这个值作为阈值二值化图像
MEDIAN_KERNEL=7
python img_process.py --point_txt=$POINT_TXT --img_path=$IMG_PATH --median_threshold=$MEDIAN_THRESHOLD --mask_threshold=$MASK_THRESHOLD --median_kernel=$MEDIAN_KERNEL

