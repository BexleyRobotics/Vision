import cv
import numpy

img = cv.LoadImage("image.jpg")
holder = cv.CreateImage(cv.GetSize(img), 8, 3)

smoothType = numpy.array([cv.CV_BLUR_NO_SCALE, cv.CV_BLUR, cv.CV_GAUSSIAN,cv.CV_MEDIAN, cv.CV_BILATERAL])

for smooth in smoothType:	
	param1 = 1 #param1 start
	while param1 <= 5:
		param2 = 1 #param2
		while param2 <= 5:
			param3 = 1 #param3	
			while param3 <= 5:
				param4 = 1 #param4
				while param4 <= 5:
					cv.Smooth(img, holder,smooth, param1, param2, param3, param4) 
					cv.SaveImage("{smoothType}-{0}-{1}-{2}-{3}.jpg".format(param1,param2, param3,param4,smoothType=smooth),holder)
					
					print "{0}-{1}-{2}-{3}-{4}".format(smooth,param1,param2,param3,param4)
					param4 = param4 + 2
				param3 = param3+2
			param2 = param2+2
		param1 = param1+2

