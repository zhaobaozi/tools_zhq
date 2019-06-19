#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
#import cv2
dict = {'go': '1', 'goForward': '2', 'goLeft': '3', 'stop': '4', 'stopLeft': '5', 'warning': '6',
        'WarningLeft': '7', 'non_of_above': '8'}
def read_csv(imput_file, out__path):
    csv = open(os.path.abspath(imput_file), 'r')
    csv.readline() # Discard the header-line.
    lines = csv.readlines()
    file_output = open(out__path+'/output.txt', 'w')
    image_name2 = ''
    for line in lines:
        Comp = line.split(';')
        Comp2 = Comp[0].split('/')
        image_name = Comp2[1]
        print(image_name)
        if image_name == image_name2:
            file_output.write(' ' + ','.join(Comp[2:6]) + ',' + Comp[1])


        else:
            file_output.write('\n' + image_name + ' ' + ','.join(Comp[2:6]) + ',' + Comp[1])
            image_name2 = image_name

    file_output.close()
    csv.close()

if __name__ == '__main__':
    
    label_file ="/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip14/frameAnnotationsBOX.csv"
    output_folder = "/home/zhaohuaqing/Downloads/LISA/dayTrain/dayClip14"
    read_csv(label_file, output_folder)

