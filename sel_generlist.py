import os
import random
import shutil
path = 'Annotations/'

def random_selectfile(srcPath, dstPath, numfiles):
    name_list=list(os.path.join(srcPath,name) for name in os.listdir(srcPath))
    random_name_list=list(random.sample(name_list,numfiles))
    i = 1
    f = open('ImageSets/Main/test.txt','w')
    for name in random_name_list:
        print name
        s = name.split('/')[-1].split('.')[0] + '\n'
        print s,i
        i = i + 1
        f.write(s)
        shutil.move(name,name.replace(srcPath, dstPath))
    f.close()

srcPath='/home/zhaobowen/darknet/VOCdevkit/VOC2007hw/Annotations'
dstPath='/home/zhaobowen/darknet/VOCdevkit/VOC2007hw/tmpxml'
random_selectfile(srcPath,dstPath,198)

dir = os.listdir(path)
f = open('ImageSets/Main/train.txt','w')
for str in dir:
	name = str.split('/')[-1].split('.')[0] + '\n'
	print name
	f.write(name)
f.close()