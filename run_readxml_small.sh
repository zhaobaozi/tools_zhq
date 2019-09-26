#!/bin/bash
IMAGE_ROOT=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/JPEGImages/
LABEL_ROOT=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/Annotations/
IMAGE_NEW=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/small/image_new/
LABEL_NEW=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/small/label_new/
IMAGE_SEE=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/small/image_see/
LABEL_NEW2=/home/zhq/cowa_zhq1/dataset/COWA/trafficlights/normal_2/small/label_new2/
python readxml_small.py $IMAGE_ROOT $LABEL_ROOT $IMAGE_NEW $LABEL_NEW $IMAGE_SEE $LABEL_NEW2

