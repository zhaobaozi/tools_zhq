# coding=utf-8
import os
import os.path
import xml.dom.minidom
FindPath = '/home/zhaohuaqing/Downloads/tl_ssd/Annotations/'
FileNames = os.listdir(FindPath)
#new_path=
#new_path = "/home/zhaohuaqing/Desktop/try/"
FileNames= os.listdir(FindPath)

for file_name in FileNames:
    if not os.path.isdir(file_name):  # 判断是否是文件夹,不是文件夹才打开
        
            if file_name.endswith('xml'):  
        #dom = xml.dom.minidom.parse(file) 
                print "ok"
                path=FindPath+file_name
                dom = xml.dom.minidom.parse(path)  

                root = dom.documentElement

    # 获取标签对name之间的值
                name = root.getElementsByTagName('name')
                for i in range(len(name)):
            #print name[i].firstChild.data
                    if name[i] .firstChild.data!= '1':
                        name[i].firstChild.data = '1'

    #将修改后的xml文件保存
                        with open(path, 'w') as fh:
                            dom.writexml(fh)
                            print(path)
