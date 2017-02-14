import cv2
import time
import numpy as np


car_cascade = cv2.CascadeClassifier('cars.xml')
cap = cv2.VideoCapture('D:/Programming/Python/image_processing/haar cascade/object detection/cars3.mp4')

#cap.set(3, 320) #width
#cap.set(4, 216) #height
#cap.set(5, 15)  #frame rate
#time.sleep(2)


#cap.set(cv.CV_CAP_PROP_FOURCC,cv.CV_FOURCC('M','P','4','2'))
while (cap.isOpened()):
    ret, img = cap.read()
    height, width, channels = img.shape
    res = cv2.resize(img,(2*width/3, 2*height/3), interpolation = cv2.INTER_CUBIC)
##    print cap.read()
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray,1.3,5)
    
    for (x,y,w,h) in cars:
        cv2.rectangle(res, (x,y), (x+w, y+h), (255,0, 0), 2)
        
    cv2.imshow('img',res)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()