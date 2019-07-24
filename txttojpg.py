import shutil
f = open("/home/zhaohuaqing/ssh/py-R-FCN1/data/VOCdevkit0712/VOC0712/ImageSets/Main/test.txt", "r")  
images='/home/zhaohuaqing/ssh/py-R-FCN1/data/VOCdevkit0712/VOC0712/JPEGImages/'
new='/home/zhaohuaqing/ssh/py-R-FCN1/data/test/new_data_all/'
while True:  
    line = f.readline()  
    if line:  
        line=line.strip('\n')
        image_path=images+line+'.jpg'
        new_path=new+line+'.jpg'
        shutil.copy(image_path,new_path)
         
         

f.close()

