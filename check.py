import glob
import xml.etree.ElementTree as ET
import os

xml_path = glob.glob('./Annotations/*.xml')
# xml_path = glob.glob('./*.xml')
save_path = './checkxml'
count = 0
i = 0
vehiclelist = ['car' , 'bus' , 'mpv' , 'truck' , 'suv' , 'van' , 'coach bus' , 'mini truck' , 'engineering vehicle' , 'tricycle' , 'tramcar']
pedestrianlist = ['person' , 'walk_person' , 'bike_person' , 'motor_person' , 'sit_person']
for path in xml_path:
	i += 1 
	flag = 0
	fname = path.split('/')[-1]
	file = open(path)
	tree = ET.parse(file)
	root = tree.getroot()
	size = root.find('size')
	w = int(size.find('width').text)
	h = int(size.find('height').text)
	for obj in root.iter('object'):
		name = obj.find('name')
		obname = name.text
		obj.remove(name)
		test = ET.Element('name')
		print obname
		if obname in vehiclelist :
			print '!!!'
			test.text = 'vehicle'
		elif obname in pedestrianlist :
			print '???'
			test.text = 'pedestrian'
		else: 
			print '--------------------------------'
		obj.insert(0,test)
        
	print fname
		# xmlbox = obj.find('bndbox')
		# xmin = int(xmlbox.find('xmin').text)
		# xmax = int(xmlbox.find('xmax').text)
		# ymin = int(xmlbox.find('ymin').text)
		# ymax = int(xmlbox.find('ymax').text)
		# if xmin <= 0 or ymin <= 0 or xmax >= w or ymax >= h:
		        # print name
			# flag = 1
			# if xmin <= 0:
				# xmlbox.find('xmin').text = str(1)
			# if ymin <= 0:
				# xmlbox.find('ymin').text = str(1)
			# if xmax >= w:
				# xmlbox.find('xmax').text = str(w-1)
			# if ymax >= h:
				# xmlbox.find('ymax').text = str(h-1)
	# if flag == 1:
		# # print name
		# count += 1
		# # tree.write(os.path.join(name), encoding='utf-8', xml_declaration=True)
	tree.write(os.path.join(save_path, fname), encoding='utf-8', xml_declaration=True)
print count
print i