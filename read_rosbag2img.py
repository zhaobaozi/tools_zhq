import rosbag
import os,sys
import cv2
from cv_bridge import CvBridge

rbag = rosbag.Bag('./image_segment_rgb.bag')

for topic,msg,t in rbag.read_messages():
        if 'image_segmentation' in topic:
        	bridge = CvBridge()
        	cv_img = bridge.imgmsg_to_cv2(msg, 'bgr8')
        	cv2.imwrite("./image_segment/{}.jpg".format(t), cv_img)
        	# os._exit(0)
rbag.close()