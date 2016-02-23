#! /usr/ben/desktop
import numpy as np
import cv2

#Get color grey in picture
#RETURNS IMAGE
def isoGrey(img, blur=true, minGrey = 128):
    #__module__ pairs down info from type(img)
    #pull image
	if(type(img).__module__ == np.__name__):
		working = np.asarray(imgp[:,:])
	else:
		working = np.copy(img)
#	if(blur):
#		cv2.blur(working, (2,2), working)
    #LIGHT BROWN IS THE FARTHEST RGB COORDINATE FROM GREY (205-183-158), although grey doesn't technically have an opposite
    #b/c grey is an inbetween color
	return cv2.inRange(working, np.array([89, 89, 89]), np.array([minGrey, minGrey, minGrey]))

#RETURNS IMAGE CON CONTSUrS
def findConts(imge):
    #find conts
    return (cnts, _) = cv2.findContours(isoGrey(imge, blur=true, minGrey = 128).copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

