## road detection with color filtering
import cv2
import numpy as np


class imageProcessing(object):
    def nothing(x):
        pass

    def __init__(self, camera, showPerson, showCar):
        """
        This is used to initialize the imageProcessing class
        :param camera: Enter which video wants to read
        :param showPerson: 1 to detect person
        :param showCar: 1 to detect car
        """
        self.showPerson = showPerson
        self.showCar = showCar
        self.cap = cv2.VideoCapture(camera)
        self.person_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
        self.car_cascade = cv2.CascadeClassifier('cars.xml')
        self.windowPrint = 0
        self.windowWid = 125
        self.windowHei = 100

    def showWindows(self):
        """
            call this function if you want to show windows
        """
        self.windowPrint = 1
        ##Create Window and Trackbar
        cv2.namedWindow('image')
        cv2.resizeWindow('image', 720, 85)
        cv2.createTrackbar('Width', 'image', 125, 1280, self.nothing)
        cv2.createTrackbar('Height', 'image', 100, 720, self.nothing)

    def printImage(self):
        """
            Call this function to show output
        :param res: entire image with navigation
        :param road: display only road wiht navigation
        :param mask: show thresholded output
        """
        if self.windowPrint == 1:
            cv2.imshow('original', self.original)
            cv2.imshow('Road', self.road)

    def image_convert(self, img):
        """

        :param img: The image which need to be converted
        :return: Road : display only the road
        resultant : Original image with resize using trackbar
        threshold : the thresholded image
        hei : height of the image
        wid : width of the image
        """
        self.windowWid = cv2.getTrackbarPos('Width', 'image')
        self.windowHei = cv2.getTrackbarPos('Height', 'image')
        if self.windowWid < 300:
            self.windowWid = 300#125
        if self.windowHei < 230:
            self.windowHei = 230#100

        ##Color change
        resultant = cv2.resize(img, (self.windowWid, self.windowHei), interpolation=cv2.INTER_CUBIC)
        blur = cv2.GaussianBlur(resultant, (5, 5), 2)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        ##hsv color range for road detection
        lower_val = np.array([100, 0, 40])
        upper_val = np.array([180, 35, 180])
        mask1 = cv2.inRange(hsv, lower_val,
                            upper_val)  # if the hsv value is in the range of lower_red and upper_red set that value to binary 1

        lower_val = np.array([0, 0, 40])
        upper_val = np.array([10, 35, 180])
        mask2 = cv2.inRange(hsv, lower_val,
                            upper_val)  # if the hsv value is in the range of lower_red and upper_red set that value to binary 1

        ##Mask for the road
        threshold = cv2.add(mask1, mask2)  # add both the binary pic into one
        kernel = np.ones((8, 8), np.uint8)
        mask = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        road = cv2.bitwise_and(resultant, resultant,
                               mask=mask)  # store only the the perticular color in the variable res
        self.road=road
        self.original=resultant
        self.threshold=mask.copy()

    def findMoment(self):
        M = cv2.moments(self.contour)
        self.cxMoment = int(M['m10'] / M['m00'])
        self.cyMoment = int(M['m01'] / M['m00'])
        self.currentError = self.cxMoment - self.roadWidth / 2

    def drawMoment(self):
        self.findMoment()
        cv2.line(self.original, (self.cxMoment, self.cyMoment), (self.windowWid / 2, self.windowHei), (0, 0, 255),2)
        cv2.line(self.road, (self.cxMoment, self.cyMoment), (self.windowWid / 2, self.windowHei), (0, 0, 255),2)

    def drawCenterLine(self):
        ##draw  Center line
        cv2.line(self.original, (self.windowWid / 2, 0), (self.windowWid / 2, self.windowHei), (255, 0, 0),1)
        cv2.line(self.road, (self.windowWid / 2, 0), (self.windowWid / 2, self.windowHei), (255, 0, 0),1)

    def drawLine(self,cx,cy):
        ##draw required line
        cv2.line(self.original, (cx, cy), (self.windowWid / 2, self.windowHei), (0, 0, 255),2)
        cv2.line(self.road, (cx, cy), (self.windowWid / 2, self.windowHei), (0, 0, 255),2)

    def car_rect(self, res):
        '''
        This function will draw a rectangle around the car
        :param res: the original image who needs to be converted
        :param car_cascade: the object for the car cascade
        :return res: the converted image
        '''
        # convert to gray
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # find cars
        cars = self.car_cascade.detectMultiScale(gray, 1.3, 5)

        # draw rectangle
        for (x, y, w, h) in cars:
            cv2.rectangle(res, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return res

    def person_rect(self, res):
        '''
        This function will draw a rectangle around any perosn that it detect
        :param res: the original image who needs to be converted
        :param person_cascade: the object for the person cascade
        :return res: the converted image
        '''
        # convert to gray
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # find cars
        persons = self.person_cascade.detectMultiScale(gray, 1.3, 5)

        # draw rectangle
        for (x, y, w, h) in persons:
            cv2.rectangle(res, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return res

    def capCheck(self):
        """
        This is used to check whether video is opened or not
        :return: 1 if video is opened
        """
        return self.cap.isOpened()

    def imagePreprocessing(self):
        ##Read video and cascade file
        size, img = self.cap.read()
        if size == 0:
            print("The END")
            cv2.destroyAllWindows()
            return 0

        self.image_convert(img)

        ## Coutour
        contours, hierarchy = cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(c) for c in contours]  # Find the index of the largest contour
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        self.roadWidth = w
        self.contour=cnt
        cv2.drawContours(self.original, contours, max_index, (0, 255, 0), 3)


        ##detect cars
        if (self.showCar == 1):
            self.original = self.car_rect(self.original)
        if (self.showPerson == 1):
            self.original = self.person_rect(self.original)

        ##show the output

    def destroy(self):
        cv2.destroyAllWindows()
        self.cap.release()


if __name__ == "__main__":
    road = imageProcessing('vid2.mp4', 0, 0)
    road.showWindows()
    while road.capCheck():
        road.imagePreprocessing()
        road.drawCenterLine()
        road.drawMoment()
        road.printImage()
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    road.destroy()
