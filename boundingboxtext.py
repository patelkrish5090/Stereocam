import cv2
import numpy as np



def show_rectangle(img,x,y,w,h):
    img =  cv2.rectangle(img,(x,y),(x+w,y+h),5)
    cv2.imshow('image',img)
    cv2.waitKey(300)
    cv2.destroyAllWindows


class Sterocam():
    def __init__(self):
        self.ycenter = 0

    def getContours(self,img):
        imgContour = img
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
        imgCanny = cv2.Canny(imgBlur,50,50)
        contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        self.max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>self.max_area :
                self.max_area = area
                self.contours = cnt

        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)
        x, y, w, h = cv2.boundingRect(approx)
        self.xcenter = (x + (w/2))
        self.ycenter = (y + (h/2))
        return x, y, w, h

    
img1 = cv2.VideoCapture(4)
ref1 , frame1 = img1.read()
img2 = cv2.VideoCapture(2)
ref2,frame2 = img2.read()


camera1 = Sterocam()
camera2 = Sterocam()


x1, y1, w1 ,h1 = camera1.getContours(frame1)
x2, y2, w2, h2 = camera2.getContours(frame2)


disparity = abs(camera1.xcenter - camera2.xcenter)
fl = 3 #focal length
camdis = 3  #distance between the two camera
distance =  (fl*camdis)/disparity
print(distance)


show_rectangle(frame1,x1,y1,w1,h1)
show_rectangle(frame2,x2,y2,w2,h2)
    



