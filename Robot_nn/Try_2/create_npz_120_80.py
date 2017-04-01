__author__ = 'Abhisek Negi'

import numpy as np
import cv2
import socket

class CollectTrainingData(object):
    def __init__(self):
        self.k = np.zeros((16, 16), 'float')
        for i in range(16):
            self.k[i, i] = 1
        self.collect_image()

    def processing_conn(self):
        print "Connect Processing"
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = 50009  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.process, addr = s.accept()
        print('Connected by', addr)
        self.process.sendall("0")

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
        label_array = np.zeros((1, 16), 'float')
        cv2.namedWindow('image')

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
                print img.shape

                cv2.imshow('image', img)
                # print "capturing images..."
                line = self.process.recv(1024)
                # print line,
                # print "capturing images..."
                if line == ',:;.':
                    print "."
                    if cv2.waitKey(0) == 27:
                        break
                    continue
                # print "event"
                error = self.serialEvent(line)
                print error
                if error == 1:
                    continue
                command = int("".join(map(str, error)), 2)
                print command
                img = cv2.resize(img, (120, 80))
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # select lower half of the image
                # roi = image[120:240, :]

                # save streamed images
                # cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                # cv2.imshow('roi_image', roi)
                # cv2.imshow('image', image)

                # reshape the roi image into one row array
                temp_array = image.reshape(1, 9600)


                image_array = np.vstack((image_array, temp_array))
                label_array = np.vstack((label_array, self.k[command]))
                self.process.sendall("0")

                frame += 1
                total_frame += 1
                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    break
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/test10_del.npz', train=train, train_labels=train_labels)

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