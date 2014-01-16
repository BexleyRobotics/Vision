#! usr/bin/python
import filters
import cv


cv.NamedWindow("Positive")
cv.NamedWindow("Negative")
cv.NamedWindow("Trackbars")
cv.NamedWindow("Input")
cam = cv.CaptureFromCAM(0)

minH = 150
maxH = 204
minS = 100
maxS = 255
minV = 11
maxV = 131

def change_minH(value):
	global minH
	minH = value

def change_maxH(value):
	global maxH
	maxH = value

def change_minS(value):
	global minS
	minS = value

def change_maxS(value):
	global maxS
	maxS = value

def change_minV(value):
	global minV
	minV = value

def change_maxV(value):
	global maxV
	maxV = value

cv.CreateTrackbar("Min H", "Trackbars", minH, 255, change_minH)
cv.CreateTrackbar("Max H", "Trackbars", maxH, 255, change_maxH)
cv.CreateTrackbar("Min S", "Trackbars", minS, 255, change_minS)
cv.CreateTrackbar("Max S", "Trackbars", maxS, 255, change_maxS)
cv.CreateTrackbar("Min V", "Trackbars", minV, 255, change_minV)
cv.CreateTrackbar("Max V", "Trackbars", maxV, 255,change_maxV)
while True:
	img = cv.QueryFrame(cam)
	pos = filters.isoRed2(img,minH,minS,minV,maxH,maxS,maxV)
	neg = cv.CloneImage(pos)
	cv.AbsDiffS(neg,neg,255)
	cv.ShowImage("Positive", pos)
	cv.ShowImage("Negative", neg)
	cv.ShowImage("Input", img)
	if cv.WaitKey(5) != -1:
		print "Min: {0},{1},{2}".format(minH,minS,minV)
		print "Max: {0},{1},{2}".format(maxH,maxS,maxV)
		break
