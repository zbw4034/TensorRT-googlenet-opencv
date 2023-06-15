#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import io
import json
import glob
import cv2
#读取json
json_path = glob.glob('/home/zhaobowen/data/origindata/*/*/*.json')

bus_path = './collect/type/bus'
nonbus_path = './collect/type/nonbus'
back_path = './collect/dir/back'
left_path = './collect/dir/left'
right_path = './collect/dir/right'
forward_path = './collect/dir/forward'
other_path = './collect/dir/other'

count = 0
for path in json_path:
	s = path.split('.')[0]
	print s
	name = s.split('/')[-1]
	# print 'name =',name
	f = io.open(path,encoding = 'utf-8')
	temp = json.load(f)
	boxcount = temp['Workload']['boxCount']
	# print 'boxcount =', boxcount
	carnum = temp['Workload']['Car']
	print 'carnum =', carnum

	if carnum > 0:
		image = cv2.imread(s + '.jpg')

		for i in range(boxcount):
			val = temp['boxs'][i]
			valdata = val['val_data']
			# print valdata
			sign = valdata[0]
			# print sign
			if sign == '1':#说明为车
				count = count + 1
				print 'count =',count
				# print i,':',valdata

				cut = val['cut']
				shade = val['shade']
				if ((cut == '0') or (cut == '1') or (cut == '2'))and((shade == '0')or(shade == '1')):
					cont = val['cont']
					xmin = int(val['x'])
					ymin = int(val['y'])
					xmax = xmin + int(val['w'])
					ymax = ymin + int(val['h'])
					if (val['w']>100) or (val['h']>100):
						pic = image[ymin:ymax,xmin:xmax]
						# type = valdata[2]
						# if type =='3':
							# cv2.imwrite(os.path.join(bus_path, name + '-' + str(i) + '.jpg'),pic)
						# else:
							# cv2.imwrite(os.path.join(nonbus_path, name + '-' + str(i) + '.jpg'),pic)
						if cont == '0':
							cv2.imwrite(os.path.join(back_path, name + '-' + str(i) + '.jpg'),pic)
					# elif cont == '1':
						# cv2.imwrite(os.path.join(left_path, name + '-' + str(i) + '.jpg'),pic)
					# elif cont == '2':
						# cv2.imwrite(os.path.join(right_path, name + '-' + str(i) + '.jpg'),pic)
						elif cont == '3':
							cv2.imwrite(os.path.join(forward_path, name + '-' + str(i) + '.jpg'),pic)
						elif cont == '4':
							cv2.imwrite(os.path.join(other_path, name + '-' + str(i) + '.jpg'),pic)







