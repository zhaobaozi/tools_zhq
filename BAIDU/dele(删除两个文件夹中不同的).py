import os
def delet(path1,path2):
    filelist = os.listdir(path1)
    for item in filelist:
        item_path1=path1+item
        if item.endswith('.jpg'): 
            item_path2=path2+item
            if not os.path.exists(item_path2):
                os.remove(item_path1)
                print item_path1
        elif item.endswith('.txt'): 
            item_path2=path2+item[:-4]+'.jpg'
            if not os.path.exists(item_path2):
                os.remove(item_path1)
                print item_path1
 
if __name__ == '__main__':
    inputimagePath = '/home/zhaohuaqing/Documents/baidu/smallimages/' 
    outimagePath = '/home/zhaohuaqing/Documents/baidu/smallimages1/' 
    outxmlPath1='/home/zhaohuaqing/Documents/baidu/smalllabels/'
    outxmlPath2='/home/zhaohuaqing/Documents/baidu/smalllabelsxml/'
    #delet(outimagePath,inputimagePath)
    delet(outxmlPath1,inputimagePath)
    delet(outxmlPath2,inputimagePath)
