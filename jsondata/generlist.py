import os
path = './data/xml/'
dir = os.listdir(path)
f = open('./train.txt','w')
for str in dir:
	name = str.split('/')[-1].split('.')[0] + '\n'
	print name
	f.write(name)
f.close()