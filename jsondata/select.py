import random
import os
import shutil

# def random_movefile(srcxmlPath,dstxmlPath,srcimgPath,dstimgPath,numfiles):
    # name_list=list(os.path.join(srcxmlPath,name) for name in os.listdir(srcxmlPath))
    # random_name_list=list(random.sample(name_list,numfiles))
    # if not os.path.exists(dstxmlPath):
        # os.mkdir(dstxmlPath)
    # if not os.path.exists(dstimgPath):
        # os.mkdir(dstimgPath)
    # for oldname in random_name_list:
        # print oldname
        # imgname = '/home/zhaobowen/data/data/collect/' + oldname.split('.')[0].split('/')[-1] + '.jpg'
        # print imgname
        # shutil.move(oldname,oldname.replace(srcxmlPath, dstxmlPath))
        # shutil.move(imgname,imgname.replace(srcimgPath, dstimgPath))

# srcxmlPath='/home/zhaobowen/data/data/xml'
# dstxmlPath = '/home/zhaobowen/data/detectdata/train/xml'
# srcimgPath='/home/zhaobowen/datacollect'
# dstimgPath = '/home/zhaobowen/data/detectdata/train/image'
# random_movefile(srcxmlPath,dstxmlPath,srcimgPath,dstimgPath,13685)

def random_movefile(srcPath,dstPath,numfiles):
    name_list=list(os.path.join(srcPath,name) for name in os.listdir(srcPath))
    random_name_list=list(random.sample(name_list,numfiles))
    i = 1
    if not os.path.exists(dstPath):
        os.mkdir(dstPath)
    for name in random_name_list:
        print name,i
        i = i + 1
        shutil.move(name,name.replace(srcPath, dstPath))


srcPath='/home/zhaobowen/data/data/xml'
dstPath = '/home/zhaobowen/data/tempxml'
random_movefile(dstPath,srcPath,320)