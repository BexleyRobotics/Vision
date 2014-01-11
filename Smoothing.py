import cv

img = cv.LoadImage("image.jpg")
holder = cv.CreateImage(cv.GetSize(img), 8, 3)

param1 = 1
param2 = 1
param3 = 1
param4 = 1
smoothType = "CV_BLUR"

for type in smoothType:	
	#param1 start
	while param1 < 5:
		param1 = param1 + 2

		#param2
		while param2 < 5:
			param2 = param2 + 2
		
			#param3	
			while param3 < 5:
				param3 = param3 + 2
			
				#param4
				while param4 < 5:
					cv.Smooth("image.jpg", holder, param1, param2, param3, param4) 
					cv.SaveImage("{smoothType}-{0}-{1}-{2}-{3}.jpg".format(param1,param2, param3,param4,smoothType),holder)
					param4 = param4 + 2
