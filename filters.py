#! usr/bin/python
import cv

global redmin, redmax
redmin = cv.Scalar(40,0,0)
redmax = cv.Scalar(160,100,100)

""" Isolate Color red in a picture
Args:
img: Image to be processed, can be in either format
blur: boolean whether to apply a blur on the image default: True
minRed: (Optional) Minimum color red to be filtered Default: 37
Returns Binary filtered image"""
def isoRed(img, blur=True):
	if(type(img).__module__ == cv.__name__):
		working = cv.fromarray(img)
	else:
		working = cv.CloneImage(img)

	#if(blur):
	#	cv2.blur(working, (2,2), working)

	imghsv= cv.CreateImage(cv.GetSize(img), 8, 3)
	imgthresh = cv.CreateImage(cv.GetSize(img),8,1)

	cv.CvtColor(img, imghsv, cv.CV_BGR2HSV)
	cv.InRangeS(imghsv,redmin, redmax, imgthresh)
	#cv.AbsDiffS(imgthresh,imgthresh, 255)
	return imgthresh

def isoRed2(img, hlow, slow, vlow, hhigh, shigh, vhigh):
	if(type(img).__module__ == cv.__name__):
		working = cv.fromarray(img)
	else:
		working = cv.CloneImage(img)

	#if(blur):
	#	cv2.blur(working, (2,2), working)

	imghsv= cv.CreateImage(cv.GetSize(img), 8, 3)
	imgthresh = cv.CreateImage(cv.GetSize(img),8,1)

	cv.CvtColor(img, imghsv, cv.CV_BGR2HSV)
	cv.InRangeS(imghsv,cv.Scalar(hlow,slow,vlow), cv.Scalar(hhigh,shigh,vhigh), imgthresh)
	cv.AbsDiffS(imgthresh,imgthresh, 255)
	return imgthresh

""" Isolate Color blue in a picture
Args:
img: Image to be processed, can be in either format
blur: boolean whether to apply blur on the image default: True
Returns Binary filtered image"""
def isoBlue(img, blur=True):
	if(type(img).__module__ == cv.__name__):
		working = cv.fromarray(img)
	else:
		working = cv.CloneImage(img)

	#if(blur):
	#	cv2.blur(working, (2,2), working)

	imghsv= cv.CreateImage(cv.GetSize(img), 8, 3)
	imgthresh = cv.CreateImage(cv.GetSize(img),8,1)

	cv.CvtColor(img, imghsv, cv.CV_BGR2HSV)
	cv.InRangeS(imghsv, cv.Scalar(90,50,50), cv.Scalar(120,255,255), imgthresh)
	
	return imgthresh
