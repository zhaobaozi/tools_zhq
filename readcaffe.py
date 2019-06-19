import numpy as np
import collections
from collections import OrderedDict
import caffe
caffe_model="/home/ubuntu/zhq/new/try/MobileNet-SSD-TensorRT/model/M2Det_new.caffemodel"
caffe_net="/home/ubuntu/zhq/new/try/MobileNet-SSD-TensorRT/model/M2Det_new_noplu.prototxt"
net0 = caffe.Net(caffe_net,caffe_model,caffe.TEST)
for k,v in net0.blobs.items():
    print k
    print v.data.shape

