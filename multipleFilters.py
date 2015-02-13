import cv, cv2
import Tkinter
from Tkconstants import *
import multiprocessing
cam = cv2.VideoCapture(0)
low_hsv = cv.Scalar(0, 130, 132)
high_hsv = cv.Scalar(40, 255, 255)
low_bgr = cv.Scalar(0, 88, 150)
high_bgr = cv.Scalar(129, 255, 255)
keepLooping = True
def doNothing(img):
    return img
def bilat(img):
    filtered = cv2.bilateralFilter(img, 15, 25, 25)
    return filtered
def adBilat(img):
    filtered = cv2.adaptiveBilateralFilter(img, (5, 11), 20)
    return filtered
def blur(img):
    filtered = cv2.blur(img, (15, 15))
    return filtered
def gaussBlur(img):
    filtered = cv2.GaussianBlur(img, (15, 15), 10)
    return filtered
def grayscale(img):
    filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return filtered
def bgrThresh(img):
    filtered = cv2.inRange(img, low_bgr, high_bgr)
    return filtered
def hsvThresh(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(img, low_hsv, high_hsv)
    return filtered
lookupTable = {
    "Do Nothing": doNothing,
    "Bilateral": bilat,
    "Adaptive Bilateral": adBilat,
    "Blur": blur,
    "Gaussian Blur": gaussBlur,
    "Grayscale": grayscale,
    "BGR Threshold": bgrThresh,
    "HSV Threshold": hsvThresh
}

def tkLoop(q):
    filters = ("Do Nothing","Bilateral","Adaptive Bilateral","Blur","Gaussian Blur","Grayscale","BGR Threshold","HSV Threshold")
    tk = Tkinter.Tk()
    frame = Tkinter.Frame(tk)
    frame.pack(expand=True,fill=BOTH)
    stringVars = [Tkinter.StringVar() for x in range(6)]
    for var in stringVars:
        var.set(filters[0])
    dropdowns = [Tkinter.OptionMenu(frame, stringVars[x], *filters) for x in range(6)]
    for dropdown in dropdowns:
        dropdown.pack(expand=True,fill=X)
    def fireUpdate():
        settings = [var.get() for var in stringVars]
        q.put(settings)
    def fireClose():
        global keepLooping
        keepLooping = False
        cv2.destroyAllWindows()
        tk.destroy()
    close = Tkinter.Button(frame,text="Close",command=fireClose)
    close.pack(side=BOTTOM)
    update = Tkinter.Button(frame,text="Update",command=fireUpdate)
    update.pack(side=BOTTOM)
    while keepLooping:
        tk.mainloop()
def applyFilters(q):
    while cv2.waitKey(5) == -1:
        if q.qsize() > 0:
            selectedOptions = q.get()
        #print selectedOptions
        _, orig = cam.read()
        cv2.imshow("Original",orig)
        work = orig
        for option in selectedOptions:
            work = lookupTable[option](work)
        cv2.imshow("Final",work)
if __name__ == '__main__':
    queue = multiprocessing.Queue()
    queue.put(["Do Nothing"])
    tkProc = multiprocessing.Process(target=tkLoop,args=(queue,))
    cvProc = multiprocessing.Process(target=applyFilters,args=(queue,))
    tkProc.start()
    cvProc.start()
cam.release()
