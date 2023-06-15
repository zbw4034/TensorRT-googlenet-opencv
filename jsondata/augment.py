import os
import glob
import cv2
import numpy as np
import random
img_path = glob.glob('/home/zhaobowen/data/collect/dir/left/*.jpg')
save_path = '/home/zhaobowen/pytorch_exp/image/dirdata/train/left'


for path in img_path:
	name = path.split('.')[0].split('/')[-1]
	print name
	img = cv2.imread(path)
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	a = random.uniform(0.6,0.9)
	img_hsv[:,:,1] = a * img_hsv[:,:,1]
	aug = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite(os.path.join(save_path, name + '-aug1.jpg'),aug)

	b = random.uniform(0.6,0.9)
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	img_hsv[:,1,:] = b * img_hsv[:,1,:]
	aug = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite(os.path.join(save_path, name + '-aug2.jpg'),aug)

	img_hsv[:,:,1] = a * img_hsv[:,:,1]
	aug = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite(os.path.join(save_path, name + '-aug3.jpg'),aug)