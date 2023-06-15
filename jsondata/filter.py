#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os  
import Image  
Const_Image_Format = [".jpg",".jpeg",".bmp",".png",".gif"]  
rootDir = './collect/'
#判断路径是否存在  
#os.path.exists(folderpath.encode('GBK'))路径如果存在，返回True  
limit_size = 3*1024  #图片大小限制，3K  
limit_height = 70    #高度限制  
limit_width = 70     #宽度限制  
  
class FileFilt:  
    #fileList = [""]  
    counter = 0  
    deleted = 0  
    errord = 0  
    def __init__(self):  
        pass  
    def FilterFile(self, dirr):  
        for parent,dirnames,filenames in os.walk(rootDir):         
            for filename in filenames :  
                fileDir = os.path.join(parent,filename)  
                print fileDir
                if fileDir and (os.path.splitext(fileDir)[1] in Const_Image_Format ):  
                    filesize = os.path.getsize(fileDir)  
                    if (filesize <= limit_size):  
                        os.remove(fileDir)  
                        self.deleted+=1  
                        print self.deleted
                    else:  
                        try:  
                            fp = open(fileDir,'rb')  
                            img = Image.open(fp)  
                            w,h = img.size  
                            if (w < limit_width or h < limit_height):  
                                fp.close()  
                                os.remove(fileDir)  
                                self.deleted+=1 
                                print self.deleted
                                continue  
                            #print self.counter,fileDir,'w=',w,'h=',h,',size=',(filesize/1024),'k'  
                            self.counter+=1  
                        except(IOError):  
                            fp.close()  
                            print "【ERROR】",fileDir  
                            os.remove(fileDir)  
                            self.errord+=1  
                else:  
                    os.remove(fileDir)  
                    self.deleted+=1  
  
  

if __name__ == "__main__":  
    b = FileFilt()  
    b.FilterFile(dirr = rootDir)  
    print 'count : ',b.counter  
    print 'deleted : ',b.deleted  
    print 'errord : ',b.errord  
     
    print 'execute finished.' 