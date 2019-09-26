#coding=utf-8
import os
import cv2
from PIL import Image

def unlock_movie(path):
  cap = cv2.VideoCapture(path)
  suc = cap.isOpened()  # 是否成功打开
  frame_count = 0
  while suc:
      frame_count += 1
      suc, frame = cap.read()
      params = []
      params.append(2)  # params.append(1)
      if frame_count%30==0:
          cv2.imwrite('/home/zhaohuaqing/lights_data/1/%d.jpg' % frame_count, frame, params)

  cap.release()
  print('unlock movie: ', frame_count)


if __name__ == '__main__':
  PATH_TO_MOVIES = "/home/zhaohuaqing/nfs/20190622-EQ1-13/_camera_image_raw.mp4"
  unlock_movie(PATH_TO_MOVIES)

