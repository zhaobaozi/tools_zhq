import shutil
import os
f_path="/home/zhaohuaqing/ssh/py-R-FCN1/data/VOCdevkit0712/VOC0712/ImageSets/Main/all.txt" 
#img_path="/home/zhaohuaqing/ssh/py-R-FCN1/data/VOCdevkit0712/VOC0712/JPEGImages/"
xml_path="/home/zhaohuaqing/ssh/py-R-FCN1/data/VOCdevkit0712/VOC0712/Annotations/"
test_dir="/home/zhaohuaqing/Downloads/cowa/COWA_dataset/new_test/"
count=0
f = open(f_path,"r") 
data = f.readlines() 
f.close() 
for img in os.listdir(xml_path):
    
    if img.rstrip('.xml')+'\n' not in data:
        os.remove(xml_path+img)
        print "delet:",img.rstrip('.jpg')
        


