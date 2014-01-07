#! usr/bin/python
import cv
import time

camera = cv.CaptureFromCam(0)

#Setup windows for proof of concept images
cv.NamedWindow("Realtime Image")
cv.NamedWindow("Motion Detection Image")

#Setup images to display 
frame = cv.QueryFrame(camera)
runningAvg= cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
#greyImage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
motdetectImage = cv.CloneImage(runningAvg)
diffImage

while cv.WaitKey(5) == -1:
	start = time.time()
	realtime = cv.QueryFrame(camera)
	cv.ShowImage("Realtime Image", realtime)
	
	colorImg = cv.CloneImage(realtime)
	cv.Smooth(colorImg, colorImg, cv.CV_GAUSSIAN, 19, 0)
	cv.RunningAvg(colorImg, runningAvg, 0.320)
	cv.ConvertScale(runningAvg, motdetectImage)
	cv.AbsDiff(colorImg, motdetectImage, diffImage)

	cv.ShowImage("Motion Detection Image", diffImage)
	print "Processed in % seconds." %(time.time() - start)