#! usr/bin/python
import freenect
import cv2
import cv
import numpy as np
from pynetworktables import *
import sys
import frame_convert
import time

# initialize overhead
structelem = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
x2 = 0
y2 = 0
x3 = 0
y3 = 0
xpyr = 0
ypyr = 0
chooser = SendableChooser()
start = time.time()
pic_num = 1

if len(sys.argv) != 2:
    	print("Error: specify an IP to connect to!")
    	exit(0)

ip = sys.argv[1]

NetworkTable.SetIPAddress(ip)
NetworkTable.SetClientMode()
NetworkTable.Initialize()

table = NetworkTable.GetTable(u"SmartDashboard")

def denoise(ir,structelem=structelem):
	retval, morph = cv2.threshold(ir, 30, 255, 0)
	#morph = cv.fromarray(ir)
	#cv.Erode(morph,dst=morph,iterations=2)
	#cv2.pyrDown(morph, morph)
	#cv2.pyrUp(morph, morph)
	cv2.erode(morph,structelem,morph,(-1,-1),2)
	cv2.dilate(morph,structelem,morph,(-1,-1),2)
	return morph

def centroid(morph):
	contours,hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	x3 = 0
	y3 = 0
	x2 = 0
	y2 = 0
	xpyr = 0
	ypyr = 0
	high_area = 0.0
	second_area = 0.0
	pyr_area = 0.0

	for cnt in contours:
		moments = cv2.moments(cnt)                          # Calculate moments
		if moments['m00'] > second_area:
			if moments['m00'] > high_area:
				second_area = high_area
				high_area = moments['m00']
				x3 = x2
				y3 = y2
		    		x2 = int(moments['m10']/moments['m00'])         # cx = M10/M00
				y2 = int(moments['m01']/moments['m00'])         # cy = M01/M00
			else:
				second_area = moments['m00']
				x3 = int(moments['m10']/moments['m00'])
				y3 = int(moments['m01']/moments['m00'])
		if moments['m00'] > 0.0:
			if (moments['m01']/moments['m10']) > 0.5:
				if moments['m00'] > pyr_area:
					pyr_area = moments['m00']
					xpyr = int(moments['m10']/moments['m00'])         # cx = M10/M00
					ypyr = int(moments['m01']/moments['m00'])         # cy = M01/M00

	
	if second_area < 1000:
		x3 = x2
		y3 = y2
	
	table.PutNumber(u"x3", (x3-320))
	table.PutNumber(u"y3", (y3-240))
	table.PutNumber(u"x2", (x2-320))
	table.PutNumber(u"y2", (y2-240))
	table.PutNumber(u"xpyr", (xpyr-320))
	table.PutNumber(u"ypyr", (ypyr-240))
	print xpyr, ypyr
	return


table.PutNumber(u"PYRAMIDSHOT", 0)

while 1:
	ir = frame_convert.pretty_depth(freenect.sync_get_video(0, freenect.VIDEO_IR_8BIT)[0])
	morph = denoise(ir)
	centroid(morph)
	if int(time.time() - start) > pic_num:
		cv2.imwrite('/media/DISK_IMG/Robotpics/inputtest'+str(pic_num)+'.jpg',ir)
		cv2.imwrite('/media/DISK_IMG/Robotpics/filttest'+str(pic_num)+'.jpg',morph)
		pic_num+=1
	print (time.time() - start)
