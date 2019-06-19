#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
def labeled_sample(image_txt_full_path, save_txt_path,image_path):
    fr = open(image_txt_full_path,'r')
    min_est = 30
    images = fr.readlines()
    cnt = 0
    for tmp, image in enumerate(images):
        #print('{:.2f}%'.format(float(tmp+1)*100/len(images)))
        
        inx = image.find('.png')

        if inx != -1 :
#            image_name = image[:inx].split('/')[-1]
            image_name = image[:inx]
            #print(image_name)
            image_num = image_name[10:15]
            #print(image_num)
            if cnt != int(image_num):   
                diff = int(image_num)-cnt
                cnt = int(image_num)
                for h in range(1,diff+1):
                    #print h
		    n=int(image_num)-h
		    n1="%05d" % n
                    file=image_path+image_name[:10]+str(n1)+'.png'
                    #print file
                    if os.path.isfile(file) and file.find(".png")>0:
                        os.remove(file)
                        print file
               
                cnt += 1
            else:
                cnt += 1
            inx = inx+4
            corrids = image[inx:].strip('\n')

            corrids = corrids.strip()

            corrids = corrids.split(' ')

            target_num = len(corrids)

            write_full_path = save_txt_path + image_name + '.txt'

           
            wr_context = ''
            for i, corrid in enumerate(corrids):
                corrid = corrid.replace(',', ' ')
                #print(corrid)
                test_cor = corrid.split(' ')
                #print(test_cor)
                zz = test_cor[0] + ' ' + test_cor[1] + ' ' + test_cor[2] + ' ' + test_cor[3]
                #print(zz)
                zz_c = test_cor[4]
                #print(zz_c)
                #area = int(test_cor[2])*int(test_cor[3])
                #if area > min_est:
                    #wr_context = wr_context + zz_c +'-sign ' + zz + '\n'
                wr_context = wr_context + zz_c + ' ' + zz + '\n'
                #else:
            #target_num -= 1
            if target_num > 0:
                fw = open(write_full_path,'w')
                #fw.write(str(target_num) + '\n')
                fw.write(wr_context)
                fw.close()
    fr.close()

if __name__ == '__main__':
    root = '/home/zhaohuaqing/Downloads/LISA/'
    image_txt_full_path = root + 'output.txt'
    save_txt_path = root + 'labels/'
    image_path="/home/zhaohuaqing/Downloads/LISA/dayClip1/frames/"
    labeled_sample(image_txt_full_path, save_txt_path,image_path)     
    
