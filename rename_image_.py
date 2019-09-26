# -*- coding:utf8 -*-

import os
import sys
class BatchRename():
    '''
    批量重命名文件夹中的图片文件

    '''
    def __init__(self,path):
        self.path = path

    def rename(self,num):
        filelist = os.listdir(self.path) #获取文件路径
        total_num = len(filelist) #获取文件长度（个数）
        i = num  #表示文件的命名是从1开始的
        for item in filelist:
            if item.endswith('.jpg'):  #初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
                src = os.path.join(os.path.abspath(self.path), item)
                #dst = os.path.join(os.path.abspath(self.path), ''+str(i) + '.jpg')#处理后的格式也为jpg格式的，当然这里可以改成png格式
                dst = os.path.join(os.path.abspath(self.path), '00' + format(str(i), '0>4s') + '.jpg')    
                try:
                    os.rename(src, dst)
                    print ('converting %s to %s ...' % (src, dst))
                    i = i + 1
                except:
                    continue
        print ('total %d to rename & converted %d jpgs' % (total_num, i))

if __name__ == '__main__':

    demo = BatchRename(sys.argv[1])
    demo.rename(int(sys.argv[2]))
