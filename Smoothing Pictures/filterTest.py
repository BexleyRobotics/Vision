import cv

cv.NamedWindow("Threshold")
cv.NamedWindow("HSV")
cv.NamedWindow("Trackbars")
cv.NamedWindow("Input")

minH = 0
maxH = 28
minS = 29
maxS = 255
minV = 186
maxV = 255

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
cv.CreateTrackbar("Max V", "Trackbars", maxV, 255, change_maxV)

img = cv.LoadImage("0-3-3-1-3.jpg")
hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
thresh = cv.CreateImage(cv.GetSize(img), 8, 1)

cv.ShowImage("Input", img)

cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
cv.ShowImage("HSV", hsv)

while cv.WaitKey(2) == -1:
	cv.InRangeS(hsv, cv.Scalar(minH,minS,minV),cv.Scalar(maxH,maxS,maxV), thresh)
	cv.ShowImage("Threshold", thresh)

f = open("colorValues3.txt", 'w')
f.write("{0},{1},{2}\n".format(minH,minS,minV))
f.write("{0},{1},{2}\n".format(maxH,maxS,maxV))
f.close()
