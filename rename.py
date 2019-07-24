#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
 
# 获取文件夹中jpg图片的数量
def getDirImageNum(path):
    jpgDirImagesNum = 0
    for jpgfile in os.listdir(path):
        if os.path.splitext(jpgfile)[1] == '.jpg':
            jpgDirImagesNum += 1
    return jpgDirImagesNum
 
# 获取文件夹中xml文件的数量
def getDirXmlNum(path):
    xmlDirXmlNum = 0
    for xmlfile in os.listdir(path):
        if os.path.splitext(xmlfile)[1] == '.xml':
            xmlDirXmlNum += 1
    return xmlDirXmlNum
 
 
def rename(inputimagePath,inputxmlPath,outimagePath,outxmlPath):
    filelist = os.listdir(inputimagePath) # 获取文件路径
    i = getDirImageNum(outimagePath)  # 表示jpg文件的命名是从当前输出文件夹中的jpg文件数目开始的
    j = getDirXmlNum(outxmlPath) # 表示xml文件的命名是从当前输出文件夹中的xml文件数目开始的
    for item in filelist:
        if item.endswith('.jpg'):  # 初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
            src = os.path.join(os.path.abspath(inputimagePath), item)  #
            dst = os.path.join(os.path.abspath(outimagePath), '0' + format(str(i), '0>5s') + '.jpg')    # 这种情况下的命名格式为0000.jpg形式，可以自主定义想要的格式
            try:
                os.rename(src, dst)
                print ('converting %s to %s ...' % (src, dst))
                i = i + 1
            except:
                continue
            
            item1=item[:-4]+".xml"
            src2 = os.path.join(os.path.abspath(inputxmlPath), item1)
            
            if os.path.exists(src2):
                print src2
                dst2 = os.path.join(os.path.abspath(outxmlPath), '0' + format(str(j), '0>5s') + '.xml')    # 这种情况下的命名格式为0000.xml形式，可以自主定义想要的格式 
                print dst2
                try:
                # 读取xml文件
                    dom = xml.dom.minidom.parse(src2)
                    root = dom.documentElement
                    
                # 获取标签对path之间的值并赋予新值j
                    #root.getElementsByTagName('path')[0].firstChild.data = dst
                    #print ('ok')
                # 获取标签对filename之间的值并赋予新值j
                    root.getElementsByTagName('filename')[0].firstChild.data = '0' + format(str(j), '0>5s') + '.jpg'
 
                # 将修改后的xml文件保存,xml文件修改前后的路径
                # 打开并写入
                    with open(src2, 'w') as fh:
                        dom.writexml(fh)
                    
                    os.rename(src2, dst2)
                    print ('converting %s to %s ...' % (src2, dst2))
                    j = j + 1
                except:
                    continue
 
 
if __name__ == '__main__':
    inputimagePath = '/home/zhaohuaqing/Documents/rgb/new1/' 
    inputxmlPath='/home/zhaohuaqing/Documents/rgb/label1/'
    outimagePath = '/home/zhaohuaqing/Documents/rgb/images/' 
    outxmlPath='/home/zhaohuaqing/Documents/rgb/labels/'
    for root, dirs, files in os.walk(inputxmlPath):
        for file in files:
            rename(inputimagePath,inputxmlPath,outimagePath,outxmlPath)

