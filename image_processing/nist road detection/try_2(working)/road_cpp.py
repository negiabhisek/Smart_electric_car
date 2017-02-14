import cv2
import numpy as np
 
def nothing(x):
    pass
 
if __name__ == '__main__':
    #Read video and cascade file
    car_cascade = cv2.CascadeClassifier('cars.xml')
    cap = cv2.VideoCapture('../vid2.mp4')

    #Create Window and Trackbar	
    cv2.namedWindow('image')
    cv2.resizeWindow('image',720,85)
    cv2.createTrackbar('Width','image',125,1280,nothing)
    cv2.createTrackbar('Height','image',100,720,nothing)
    print cap.isOpened()
    while (cap.isOpened()):
        ret, img = cap.read()

        #resize and Convert to gray
        w = cv2.getTrackbarPos('Width','image')
        h = cv2.getTrackbarPos('Height','image')
        if w<125:
            w=125
        if h<100:
            h=100
        res = cv2.resize(img,(w, h), interpolation = cv2.INTER_CUBIC)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        
        th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #double t = 0;
    #t = (double)cvGetTickCount();//setting up timer
        kernel = np.ones((2,2),np.uint8)
        opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)    

        #find cars
        cars = car_cascade.detectMultiScale(gray,1.3,5)

        #draw rectangle
        for (x,y,w,h) in cars:
            cv2.rectangle(res, (x,y), (x+w, y+h), (255,0, 0), 2)
        
        cv2.imshow('original',res)
        cv2.imshow('Converted',thresh)
        cv2.imshow('Converted2',th3)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
