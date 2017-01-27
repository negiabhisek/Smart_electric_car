__author__ = 'Abhisek Negi'

import numpy as np
import cv2
import socket

class CollectTrainingData(object):
    def __init__(self):
        self.collect_image()

    def processing_conn(self):
        print "Connect Processing"
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = 50002  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.process, addr = s.accept()
        print('Connected by', addr)

    def serialEvent(self, line):
        # data = line[0: len(line) - 1]
        data = line
        # print data
        index1 = data.find(",", 0)
        index2 = data.find(":", 0)
        index3 = data.find(";", 0)
        index4 = data.find(".", 0)

        try:
            a00 = int(data[0: index1])
            a01 = int(data[index1 + 1: index2])
            a10 = int(data[index2 + 1: index3])
            a11 = int(data[index3 + 1: index4])
            # print angle, distance1, distance2, distance3
            # distance3 = data[index3 + 1: len(data)]

            # separated_length = map(int, angle)
            #
            # final_lenght = 0
            # for num in separated_length:
            #     final_lenght = final_lenght * 10
            #     final_lenght = final_lenght + num
            # angle = final_lenght
            # # print int(distance1)+4
            # self.iAngle1 = int(angle)
            # self.iAngle1_back = self.iAngle1
            # self.iAngle2 = 180 - self.iAngle1
            # self.iDistance1 = int(distance1)
            # self.iDistance2 = int(distance2)
            # self.iDistance3 = int(distance3)

        except:
            return 1
        return [a00,a01,a10,a11]

    def collect_image(self):
        self.processing_conn()
        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 9600))
        label_array = np.zeros((1, 4), 'float')
        cv2.namedWindow('image')

        # stream video frames one by one
        try:
            cap = cv2.VideoCapture(1)
            # print cap.set(1, 10)
            # cap.set(cv2.CV_CAP_PROP_CONVERT_RGB , false)
            # cap.set(CV_CAP_PROP_FPS, 10)
            stream_bytes = ' '
            frame = 1
            while cap.isOpened():
                ret, img = cap.read()
                line = self.process.recv(1024)
                print line
                if line == ',:;.':
                    if cv2.waitKey(0) == 27:
                        break
                error = self.serialEvent(line)
                if error == 1:
                    continue
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


                print error
                image_array = np.vstack((image_array, temp_array))
                label_array = np.vstack((label_array, error))

                frame += 1
                total_frame += 1
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/test01.npz', train=train, train_labels=train_labels)

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
