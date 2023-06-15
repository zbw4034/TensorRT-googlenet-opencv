import json

def loadlabel():
	f = open("test.json",encoding = 'utf-8')
	temp = json.load(f)
	boxcount = temp['workload']['boxcount']
	print 'boxcount =', boxcount
	carcount = temp['workload']['car']
	print 'carnum =', carcount
	imgpath = temp['img']
	print 'imgpath=', img

loadlabel()
