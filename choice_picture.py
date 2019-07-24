import cv2
import os
test_dir="/home/zhaohuaqing/Downloads/cowa/COWA_dataset/lane6/"
save_dir="/home/zhaohuaqing/Downloads/cowa/COWA_dataset/524/"
for f in os.listdir(test_dir):
    img = cv2.imread(test_dir+f)
    cv2.imshow('image',img)
    k = cv2.waitKey(0)& 0xFF
    if k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(save_dir+f,img)
    elif k == ord('w'): # wait for 's' key to save and exit
        continue

