#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import io
from xml.etree.ElementTree import ElementTree, Element
import json
import glob
import cv2
#读取json
json_path = glob.glob('/home/zhaobowen/data/origindata/*/*/*.json')
if not os.path.exists('./data/xml'):
	os.mkdir('./data/xml')
if not os.path.exists('./data/collect'):
	os.mkdir('./data/collect')
save_path = './data/xml'
collect_path = './data/collect'
count = 0
for path in json_path:
	s = path.split('.')[0]
	print s
	name = s.split('/')[-1]
	print 'name =',name
	f = io.open(path,encoding = 'utf-8')
	temp = json.load(f)
	boxcount = temp['Workload']['boxCount']
	# print 'boxcount =', boxcount
	carnum = temp['Workload']['Car']
	pernum = temp['Workload']['Pedestrians']
	print 'carnum =', carnum
	print 'pernum =', pernum
	if carnum > 0 or pernum > 0:
		count = count + 1
		print count
		tree = ElementTree()
		tree.parse('/home/zhaobowen/data/demo.xml')
		file_name = tree.find('filename')
		file_name.text = name + '.jpg'
		image = cv2.imread(s + '.jpg')
		cv2.imwrite(os.path.join(collect_path, name + '.jpg'),image)
		height = image.shape[0]
		width = image.shape[1]
		for size in tree.findall('size'):
			size.find('width').text = str(width)
			size.find('height').text = str(height)
		for i in range(boxcount):
			val = temp['boxs'][i]
			sign = val['val_data'][0]
			if sign == '0' or sign == '1':
				key = val['val_data1'] if 'val_data1' in val else ""
				print i,':',key
				cut = val['cut']
				shade = val['shade']
				if ((cut == '0') or (cut == '1') or (cut == '2'))and((shade == '0')or(shade == '1')):
			#读取属性

					xmin = int(val['x'])
					ymin = int(val['y'])
					xmax = xmin + int(val['w'])
					ymax = ymin + int(val['h'])



			#建立新的object分支
					obj = Element('object')
					x_obj_name = Element('name')

					x_bndbox = Element('bndbox')
					x_xmin = Element('xmin')
					x_ymin = Element('ymin')
					x_xmax = Element('xmax')
					x_ymax = Element('ymax')

					if sign == '0':
						x_obj_name.text = 'pedestrian'
					else:
						x_obj_name.text = 'vehicle'
					x_xmin.text = str(xmin)
					x_ymin.text = str(ymin)
					x_xmax.text = str(xmax)
					x_ymax.text = str(ymax)

					x_bndbox.append(x_xmin)
					x_bndbox.append(x_ymin)
					x_bndbox.append(x_xmax)
					x_bndbox.append(x_ymax)

					obj.append(x_obj_name)
					obj.append(x_bndbox)

					root = tree.getroot()
					root.append(obj)

		tree.write(os.path.join(save_path, name + '.xml'), encoding='utf-8', xml_declaration=True)


