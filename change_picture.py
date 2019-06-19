import os
import cv2
picture_path='/home/zhaohuaqing/Documents/cam0/'
new_path='/home/zhaohuaqing/Documents/rgb/new0_0/'

def change(f,b,g,r):
    path=picture_path+f
    newpath=new_path+f
    img=cv2.imread(path,cv2.IMREAD_COLOR)
    img[:,:,0]=img[:,:,0]*b
    img[:,:,1]=img[:,:,1]*g
    img[:,:,2]=img[:,:,2]*r
    cv2.imwrite(newpath,img)
    
if __name__ == '__main__':
    b=0.90625
    g=0.671875
    r=0.8984375
    for f in os.listdir(picture_path):
        change(f,b,g,r)

