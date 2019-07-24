# -*- coding: utf-8 -*-
import os
import random
if __name__ == '__main__':
    path = '/home/zhaohuaqing/py/py-R-FCN1/data/VOCdevkit0712/VOC0712/718'
    dataAnnotated = os.listdir(path + '/Annotations')
    random.shuffle(dataAnnotated)
    dataNum = len(dataAnnotated)
 
    ftest = open('ImageSets/Main/test.txt', 'w')
    ftrain = open('ImageSets/Main/train.txt', 'w')
    ftrainval = open('ImageSets/Main/trainval.txt', 'w') 
    fval = open('ImageSets/Main/val.txt', 'w')
    testScale = 0.0001
    trainScale = 0.9999

    i = 1
    testNum = int(dataNum * testScale)
    trainNum = int((dataNum - testNum) * trainScale) 

    for name in dataAnnotated:
        if i <= testNum:
            print>>ftest, name[0:6]
        elif i <= testNum + trainNum:
            print>>ftrain, name[0:6]
            print>>ftrainval, name[0:6]
        else:
            print>>fval, name[0:6]
            print>>ftrainval, name[0:6]
        i += 1
    ftrain.close
    ftrainval.close
    fval.close
    ftest.close
    print 'done!'


