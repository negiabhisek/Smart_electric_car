## road detection with color filtering
import cv2
import numpy as np


def nothing(x):
        pass


def print_image(res, road, mask, ):
        cv2.imshow('original', res)
        cv2.imshow('Road', road)
        cv2.imshow('threshold', mask)


def image_convert(img):
        """

        :param img: The image which need to be converted
        :return: Road : display only the road
        resultant : Original image with resize using trackbar
        threshold : the thresholded image
        hei : height of the image
        wid : width of the image
        """
        wid = cv2.getTrackbarPos('Width', 'image')
        hei = cv2.getTrackbarPos('Height', 'image')
        if wid < 125:
                wid = 125
        if hei < 100:
                hei = 100

        ##Color change
        resultant = cv2.resize(img, (wid, hei), interpolation=cv2.INTER_CUBIC)
        blur = cv2.GaussianBlur(resultant, (5, 5), 2)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        ##hsv color range for road detection
        lower_val = np.array([100, 0, 40])
        upper_val = np.array([180, 35, 180])
        mask1 = cv2.inRange(hsv, lower_val,upper_val)  # if the hsv value is in the range of lower_red and upper_red set that value to binary 1

        lower_val = np.array([0, 0, 40])
        upper_val = np.array([10, 35, 180])
        mask2 = cv2.inRange(hsv, lower_val,upper_val)  # if the hsv value is in the range of lower_red and upper_red set that value to binary 1

        ##Mask for the road
        threshold = cv2.add(mask1, mask2)  # add both the binary pic into one
        kernel = np.ones((8, 8), np.uint8)
        closing = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        mask = closing.copy()
        road = cv2.bitwise_and(resultant, resultant, mask=mask)  # store only the the perticular color in the variable res

        return road, resultant, threshold, (hei, wid)


def draw_line(resultant, contour, wid, hei, y, w):
        roi = resultant[(y + h / 2):, :]
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        ##draw  Center line
        cv2.line(resultant, (wid / 2, y), (wid / 2, hei), (255, 0, 0), w / 300)

        ##draw required line
        cv2.line(resultant, (cx, cy), (wid / 2, hei), (0, 0, 255), w / 300)
        return resultant, cx

def car_rect(res,car_cascade):
        '''
        This function will draw a rectangle around the car 
        :param res: the original image who needs to be converted
        :param car_cascade: the object for the car cascade
        :return res: the converted image
        '''
        #convert to gray
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #find cars
        cars = car_cascade.detectMultiScale(gray,1.3,5)

        #draw rectangle
        for (x,y,w,h) in cars:
                cv2.rectangle(res, (x,y), (x+w, y+h), (255,0, 0), 2)

        return res

def person_rect(res,person_cascade):
        '''
        This function will draw a rectangle around any perosn that it detect
        :param res: the original image who needs to be converted
        :param person_cascade: the object for the person cascade
        :return res: the converted image
        '''
        #convert to gray
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #find cars
        cars = car_cascade.detectMultiScale(gray,1.3,5)

        #draw rectangle
        for (x,y,w,h) in cars:
                cv2.rectangle(res, (x,y), (x+w, y+h), (255,0, 0), 2)

        return res

        
if __name__ == "__main__":
        ##Read video and cascade file
        person_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
        car_cascade = cv2.CascadeClassifier('cars.xml')
        cap = cv2.VideoCapture('../vid2.mp4')
        

        ##Create Window and Trackbar
        cv2.namedWindow('image')
        cv2.resizeWindow('image', 720, 85)
        cv2.createTrackbar('Width', 'image', 125, 1280, nothing)
        cv2.createTrackbar('Height', 'image', 100, 720, nothing)

        while cap.isOpened():
                size, img = cap.read()
                if size == 0:
                        print("The END")
                        cv2.destroyAllWindows()
                        break

                road, resultant, threshold, (hei, wid) = image_convert(img)

                ##Coutour
                contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                areas = [cv2.contourArea(c) for c in contours]  # Find the index of the largest contour
                max_index = np.argmax(areas)
                cnt = contours[max_index]
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.drawContours(resultant, contours, max_index, (0, 255, 0), 3)

                ##findout centroid and draw line
                resultant, cx = draw_line(resultant, cnt, wid, hei, y, w)

                road, cx = draw_line(road, cnt, wid, hei, y, w)

                if (abs(cx - wid/2)) < (wid / 80):
                        print("go: Straight")
                elif cx > wid / 2:
                        print("go: Right: " + str(abs(cx-wid/2)))
                else:
                        print("go: Left: " + str(abs(cx-wid/2)))

                ##detect cars
                resultant = car_rect(resultant,car_cascade)
                resultant = person_rect(resultant,person_cascade)
                ##show the output
                print_image(resultant, road, threshold)
                ##wait for any key to press
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                        break

        cv2.destroyAllWindows()
        cap.release()
