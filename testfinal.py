#! usr/bin/python
import freenect
import cv2
import cv
import numpy as np
import frame_convert as fc
import time
from pynetworktables import *

# initialization overhead
global ir, depth, x3, y3, x2, y2, xpyr, ypyr, ctx, angle, structelem, morph, distwall, distpyr, momenta3, momentsa2, momentapyr
structelem = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#ctx = freenect.init()
x2 = 0
y2 = 0
x3 = 0
y3 = 0
xpyr = 0
ypyr = 0
distwall = 0
distpyr = 0
momenta3 = 0
momenta2 = 0
momentapyr = 0
angle = 0
cv2.namedWindow('input')

SmartDashboard.init()
chooser = SendableChooser()
chooser.AddObject(u'choice1', u'number1')
chooser.AddDefault(u'choice2', u'number2')
SmartDashboard.Putdata(u'choose', chooser)

def grab():
	global depth, ir
	start = time.time()
	ir = fc.pretty_depth(freenect.sync_get_video(0, freenect.VIDEO_IR_8BIT)[0])
	cv2.imshow("input", ir)
	depth = fc.pretty_depth(freenect.sync_get_depth()[0])
	#freenect.sync_stop()
	print 'grab ' + str(time.time() - start)
	#ir = cv2.imread('PyrIR7.jpg')
	#depth = cv2.imread('PyrDepth7.jpg')

def denoise():
	global ir, morph
	#start = time.time()
	cv2.threshold(ir, 20, 255, 0, ir)
	morph = cv2.morphologyEx(ir, cv2.MORPH_OPEN, structelem)
	cv2.pyrDown(morph, morph)
	cv2.pyrUp(morph, morph)
	cv2.threshold(morph, 220, 255, 0, morph)
	#print 'thresh ' + str(time.time() - start)

def centroid23():
	global morph,x3,y3, x2, y2, momenta3, momenta2
	#start = time.time()
	#temp = cv2.cvtColor(morph, cv2.COLOR_BGR2GRAY)
	contours,hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	high_area = 0.0
	second_area = 0.0
	n = 0
	for cnt in contours:
		moments = cv2.moments(cnt)                          # Calculate moments
		if moments['m00'] > momenta3:
			if moments['m00'] > momenta2:
				momenta3 = momenta2
				momenta2 = moments['m00']
				x3 = x2
				y3 = y2
		    		x2 = int(moments['m10']/moments['m00'])         # cx = M10/M00
				y2 = int(moments['m01']/moments['m00'])         # cy = M01/M00
				if n < 1:
					distwall = depth[y2][x2]
				n += 1
			else:
				momenta3 = moments['m00']
				x3 = int(moments['m10']/moments['m00'])
				y3 = int(moments['m01']/moments['m00'])
	
	'''
	x3 = '%03d' % int(x3)
	y3 = '%03d' % int(y3)
	x2 = '%03d' % int(x2)
	y2 = '%03d' % int(y2)
	momenta3 = '%05d' % int(momenta3)
	momenta2 = '%05d' % int(momenta2)
	'''
	if momenta3 < 1000:
		momenta3 = momenta2
		x3 = x2
		y3 = y2
	#print '2/3 point ' + str(time.time() - start)
	#if x3 > 0:
	#	x3 = '+' + str(x3)
	#if y3 > 0:
	#	y3 = '+' + str(y3)
	#if x2 > 0:
	#	x2 = '+' + str(x2)
	#if y2 > 0:
	#	y2 = '+' + str(y2)


def centroidpyr():
	global morph,ir, x3, y3, x2, y2, xpyr, ypyr, momentapyr
	start = time.time()
	n = 0
	pyr = ir
	y = (y3 - 25)
	loop = time.time()
	while y < 480 and y < (y3+25):
		x = (x3 - 75)
		while x < 640 and x < (x3+75):
			if morph[y][x] > 10:
				pyr[y][x] = 0
			x += 1
		y += 1
	#print 'loop1 ' + str(time.time() - loop)
	y = (y2 - 25)
	loop = time.time()
	while y < 480 and y < (y2 + 25):
		x = (x2 - 75)
		while x < 640 and x < (x2+75):
			if morph[y][x] > 10:
				pyr[y][x] = 0
			x += 1
		y += 1
	#print 'loop2 ' + str(time.time() - loop)
	cv2.GaussianBlur(pyr,(5,5), 5, pyr)
	cv2.threshold(pyr, 50, 255, 0, pyr)
	contours,hierarchy = cv2.findContours(pyr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	high_area = 0.0
	n = 0
	for cnt in contours:
		moments = cv2.moments(cnt)                          # Calculate moments
		if moments['m00'] > momentapyr:
			momentapyr = moments['m00']
		    	xpyr = int(moments['m10']/moments['m00'])         # cx = M10/M00
			ypyr = int(moments['m01']/moments['m00'])         # cy = M01/M00
			if n < 1:
				distpyr = depth[ypyr][xpyr]
				n+=1
	
	#xpyr = '%03d' % int(xpyr)
	#ypyr = '%03d' % int(ypyr)
	print 'Pyramid ' + str(time.time() - start)
	cv2.imwrite('pyrfiltersample.jpg', pyr)
	#if xpyr > 0:
	#	xpyr = '+' + str(xpyr)
	#if ypyr > 0:
	#	ypyr = '+' + str(ypyr)


def accel(times=20):
	global ctx, angle
	#start = time.time()
	dev = freenect.open_device(ctx, 0)
	angle = 0
	passes = times
	while passes > 0:
		freenect.update_tilt_state(dev)
		angle += freenect.get_tilt_degs(freenect.get_tilt_state(dev))
		passes -= 1
	angle = round((angle/times) , 1)
	freenect.close_device(dev)
	#print 'accel ' + str(time.time() - start)

def write():
	
	values = '%s %03d %03d %04d %05d %03d %03d %05d %03d %03d %04d %05d' % (angle,(x3-640),(y3-480),distwall,momenta3,(x2-640),(y2-480),momenta2,(xpyr-640),(ypyr-480),distpyr,momentapyr)
	SmartDashboard.PutNumber(u'test', values)


while 1:
	start = time.time()
	grab()
	#accel(5)
	denoise()
	centroid23()
	centroidpyr()
	write()
	print 'all ' + str(time.time() - start) + '\n'
	time.sleep(1)

