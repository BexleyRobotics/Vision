import freenect, frame_convert
import cv2
import cv
import time
'''
cv.NamedWindow('Image_Window', cv.CV_WINDOW_AUTOSIZE)
capture=cv.CaptureFromCAM(0)
image=cv.QueryFrame(capture)
cv.ShowImage('Image_Window',image)
cv.WaitKey(5000)
cv.SaveImage('image.png', image)

inp = -1
while(inp == -1):
	cv2.namedWindow('Test')
	img = frame_convert.pretty_depth(freenect.sync_get_video(0,freenect.VIDEO_IR_8BIT)[0])
	cv2.imshow('Test',img)
	inp = cv2.waitKey(100)
freenect.sync_stop()
'''

cam = cv2.VideoCapture(0)
t0 = time.time()
for x in range(1000):
	_, img = cam.read()

t1 = time.time()
print "Using read(): {0} fps".format(1000/(t1-t0))

t0 = time.time()
for x in range(1000):
	_ = cam.grab()
	_, img = cam.retrieve()

t1 = time.time()
print "Using grab() + retrieve(): {0} fps".format(1000/(t1-t0))
