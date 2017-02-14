#road detection with color filtering
import cv2
import numpy as np

def nothing(x):
    pass

#Read video and cascade file
car_cascade = cv2.CascadeClassifier('cars.xml')
cap = cv2.VideoCapture('../vid2.mp4')

#Create Window and Trackbar
cv2.namedWindow('image')
cv2.resizeWindow('image',720,85)
cv2.createTrackbar('Width','image',125,1280,nothing)
cv2.createTrackbar('Height','image',100,720,nothing)

while (cap.isOpened()):
    _,img = cap.read()

    #resize and Convert to HSV
    w = cv2.getTrackbarPos('Width','image')
    h = cv2.getTrackbarPos('Height','image')
    if w<125:
        w=125
    if h<100:
        h=100

    #Color change
    res = cv2.resize(img,(w, h), interpolation = cv2.INTER_CUBIC)
    blur=cv2.GaussianBlur(res,(5,5),2)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    #hsv color range for road detection
    lower_val = np.array([90,10,0])
    upper_val = np.array([180,20,255])
    mask1 = cv2.inRange(hsv,lower_val,upper_val)    #if the hsv value is in the range of lower_red and upper_red set that value to binary 1
    
    lower_val = np.array([0,10,0])
    upper_val = np.array([10,20,255])
    mask2 = cv2.inRange(hsv,lower_val,upper_val)    #if the hsv value is in the range of lower_red and upper_red set that value to binary 1

    #Mask for the road
    mask=cv2.add(mask1,mask2)                       #add both the binary pic into one
    kernel = np.ones((8,8),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask=closing.copy()
    road = cv2.bitwise_and(res,res,mask=mask)    #store only the the perticular color in the variable res

    #show the output
    cv2.imshow('original',res)
    cv2.imshow('img',road)
    cv2.imshow('threshold',mask)
    
    #wait for any key to press
    k=cv2.waitKey(5) & 0xFF
    if k==27:
        break

cv2.destroyAllWindows()
cap.release()
