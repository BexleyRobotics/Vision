#! usr/bin/python
import numpy as np
import cv2

""" Isolate Color red in a picture
Args:
img: Image to be processed, can be in either format
blur: boolean whether to apply a blur on the image default: True
minRed: (Optional) Minimum color red to be filtered Default: 37
Returns Binary filtered image"""
def isoRed(img, blur=True, minRed=37):
	if(type(img).__module__ == np.__name__):
		working = np.asarray(img[:,:])
	else:
		working = np.copy(img)

	if(blur):
		cv2.blur(working, (2,2), working)
	
	iso = cv2.inRange(working, np.array([0,0,minRed]),np.array([10,25,255]))
	return iso

""" Isolate Color blue in a picture
Args:
img: Image to be processed, can be in either format
blur: boolean whether to apply blur on the image default: True
Returns Binary filtered image"""
def isoBlue(img, blur=True):
	if(type(img.__module__ == np.__name__):
		working = np.asarray(img[:,:])
	else:
		working = np.copy(img)

	if(blur):
		cv2.blur(working, (2,2), working)

	iso = cv2.inRange(working, np.array([0,20,20]), np.array([255,50,50]))
	return iso
