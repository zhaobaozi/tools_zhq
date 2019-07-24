#!/bin/bash
PCL_PATH=../../data/cloud_cluster_1.pcd #输入需要提取马路牙子的点云
IMG_SAVE_PATH=../../result/2d_img.jpg  #输出点云投影的二维图
HAVE_POINT=0 #首次运行设置为0，即先提取马路牙子二维坐标，然后再设置为1，即根据坐标转换到三维点云中显示
TXT_PATH=../../result/point.txt #输出马路牙子二维坐标
mkdir result
cd get_point
catkin_make
cd build
 ./get_point $PCL_PATH $IMG_SAVE_PATH $HAVE_POINT $TXT_PATH 

