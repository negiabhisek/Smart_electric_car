__author__ = 'Abhisek Negi'

import numpy as np
import cv2


class CollectTrainingData(object):
    def __init__(self):
        self.x = "no"
        self.k = np.zeros((2,2), 'float')
        for i in range(2):
            self.k[i, i] = 1
        self.collect_image()


    def data(self, event, x, y, flags, param):
        if x<40:
            self.x = "left"
        else:
            self.x = "right"
        # if event == cv2.EVENT_FLAG_LBUTTON:
        #     self.x = "left"
        # elif event == cv2.EVENT_FLAG_SHIFTKEY:
        #     self.x = "right"

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 9600))
        label_array = np.zeros((1, 2), 'float')
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',self.data)

        # stream video frames one by one
        try:
            cap = cv2.VideoCapture(0)
            # print cap.set(1, 10)
            # cap.set(cv2.CV_CAP_PROP_CONVERT_RGB , false)
            # cap.set(CV_CAP_PROP_FPS, 10)
            stream_bytes = ' '
            frame = 1
            while cap.isOpened():
                ret, img = cap.read()
                img = cv2.resize(img, (120, 80))
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # select lower half of the image
                # roi = image[120:240, :]

                # save streamed images
                cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                # cv2.imshow('roi_image', roi)
                cv2.imshow('image', image)

                # reshape the roi image into one row array
                temp_array = image.reshape(1, 9600)

                # get the data back and check
                # ig = temp_array.copy()
                # img2 = ig.reshape(120, 320)
                # print img2.shape
                # cv2.imshow("image", img2)

                if self.x == "left":
                    self.x = "no"
                    print "LEFT"
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[0]))
                    saved_frame += 1
                elif self.x == "right":
                    self.x = "no"
                    print "right"
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[1]))
                    saved_frame += 1

                frame += 1
                total_frame += 1
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/test08.npz', train=train, train_labels=train_labels)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    CollectTrainingData()
