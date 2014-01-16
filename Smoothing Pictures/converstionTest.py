#! usr/bin/python

import cv

filt = 0
while filt < 5:
	one = 1
	while one <= 5:
		two = 1
		while two <= 5:
			three = 1
			while three <= 5:
				four = 1
				while four <= 5:
					img = cv.LoadImage("{0}-{1}-{2}-{3}-{4}.jpg".format(filt,one,two,three,four))
					hsv = cv.CreateImage(cv.GetSize(img),8,3)
					cv.CvtColor(img,hsv, cv.CV_BGR2HSV)			
					#thresh = cv.CreateImage(cv.GetSize(img),8,1)
					#cv.InRangeS(hsv, cv.Scalar(150,100,11), cv.Scalar(204,255,131),thresh)
					#cv.SaveImage("thresh-{0}-{1}-{2}-{3}-{4}.jpg".format(filt,one,two,three,four), thresh)
					cv.SaveImage("hsv-{0}-{1}-{2}-{3}-{4}.jpg".format(filt,one,two,three,four), hsv)
					four = four+2
				three = three+2
			two = two + 2
		one = one + 2
	filt = filt + 1
