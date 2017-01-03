import cv2
import numpy as np
from time import sleep
#import serial
import math
import socket


class draw_lidar:
    def __init__(self, range):
        self.img = np.zeros((700, 1366, 3), np.uint8)
        self.img[:] = (40, 8, 7)
        self.range = range

        cv2.line(self.img, (0, 236), (1366, 236), (255, 0, 0), 2)
        cv2.line(self.img, (0, 473), (1366, 473), (255, 0, 0), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.img, str(range) + ' Meter', (1230, 27), font, 1, (255, 255, 255), 2)
        cv2.putText(self.img, str(range * 2 / 3) + ' Meter', (1230, 263), font, 1, (255, 255, 255), 2)
        cv2.putText(self.img, str(range / 3) + ' Meter', (1230, 500), font, 1, (255, 255, 255), 2)

        self.prev_x1 = 683
        self.prev_y1 = 700

        self.prev_x2 = 683
        self.prev_y2 = 700

        self.prev_x3 = 683
        self.prev_y3 = 700

        self.max_val = 0

    def processing_conn(self):
        print "Connect Processing"
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = 50019  # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        self.process, addr = s.accept()
        print('Connected by', addr)

    def matlab_conn(self):
        print "Connect MATLAB"
        HOST = 'localhost'
        PORT = 7013
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print "waiting for response from client at port ", PORT
        self.matlab, addr = s.accept()
        print 'Connected to', addr

    def file_conn(self):
        self.fobj = open("data_lidar.txt")

    def arduino_conn(self):
        available = []
        for i in range(256):
            try:
                s = serial.Serial("COM" + str(i), 9600)
                available.append((i, s.portstr))
                s.close()
            except serial.SerialException:
                print str(i) + 'failed'
                pass
        return available

    def cal_converge1(self):

        c = math.sqrt(53 ** 2 + self.iDistance1 ** 2 - 2 * 53 * self.iDistance1 * math.cos(math.radians(self.iAngle1)))
        y = math.degrees(math.asin((self.iDistance1 * math.sin((math.radians(self.iAngle1)))) / c))
        if self.iAngle1 > 90:
            self.iAngle1 = 180 - y
        else:
            self.iAngle1 = y
        self.iDistance1 = c
        # print c, y

    def cal_converge3(self):
        self.iAngle1 = 180 - self.iAngle1
        c = math.sqrt(53 ** 2 + self.iDistance3 ** 2 - 2 * 53 * self.iDistance3 * math.cos(math.radians(self.iAngle1)))
        # print c,
        y = math.degrees(math.asin((self.iDistance3 * math.sin((math.radians(self.iAngle1)))) / (c)))
        # y=y+30.0
        y = 180 - y
        self.iDistance3 = c
        if self.iAngle1 > 90:
            self.iAngle1 = 180 - y
        else:
            self.iAngle1 = y
            # print y

    def draw_dot1(self, img):
        self.cal_converge1()
        cv2.circle(img, (self.prev_x1, self.prev_y1), 4, (50, 50, 0), -1)
        #  cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        x1 = int(self.iDistance1 * np.math.cos(np.math.radians(self.iAngle1)))
        y1 = int(self.iDistance1 * np.math.sin(np.math.radians(self.iAngle1)))
        self.max_val = y1
        # print "y1=", y1
        x_px = (700.0 / (self.range * 100.0)) * float(x1)
        y_px = (700.0 / (self.range * 100.0)) * float(y1)
        # print "dot1=",
        # print x1, x_px, y1, y_px
        x_px = int(683 - x_px)
        y_px = int(700 - y_px)
        # print "dot1=",
        # print x1, x_px, y1, y_px
        cv2.circle(img, (x_px, y_px), 3, (250, 255, 0), -1)
        self.prev_x1 = x_px
        self.prev_y1 = y_px
        return img

    def draw_dot2(self, img):
        cv2.circle(img, (self.prev_x2, self.prev_y2), 4, (0, 50, 0), -1)
        #  cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        x = int(self.iDistance2 * np.math.cos(np.math.radians(self.iAngle2)))
        y = int(self.iDistance2 * np.math.sin(np.math.radians(self.iAngle2)))
        if y > self.max_val:
            self.max_val = y
        # print "y2=", y
        x_px = (700.0 / (self.range * 100.0)) * float(x)
        y_px = (700.0 / (self.range * 100.0)) * float(y)
        x_px = int(683 - x_px)
        y_px = int(700 - y_px)
        # print "dot2=",
        # print x, x_px, y, y_px
        cv2.circle(img, (x_px, y_px), 3, (0, 255, 0), -1)
        self.prev_x2 = x_px
        self.prev_y2 = y_px
        return img

    def draw_dot3(self, img):
        self.iAngle1 = self.iAngle1_back
        self.cal_converge3()
        cv2.circle(img, (self.prev_x3, self.prev_y3), 4, (0, 50, 50), -1)
        # cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        x = int(self.iDistance3 * np.math.cos(np.math.radians(self.iAngle1)))
        y = int(self.iDistance3 * np.math.sin(np.math.radians(self.iAngle1)))
        if y > self.max_val:
            self.max_val = y
        # print "y3=", y
        x_px = (700.0 / (self.range * 100.0)) * float(x)
        y_px = (700.0 / (self.range * 100.0)) * float(y)
        x_px = int(683 - x_px)
        y_px = int(700 - y_px)
        # print "dot3=",
        # print x, x_px, y, y_px
        cv2.circle(img, (x_px, y_px), 3, (0, 255, 250), -1)
        self.prev_x3 = x_px
        self.prev_y3 = y_px
        return img

    def serialEvent(self, line):
        # data = line[0: len(line) - 1]
        data = line
        # print data
        index1 = data.find(",", 0)
        index2 = data.find(":", 0)
        index3 = data.find(";", 0)
        index4 = data.find(".", 0)

        angle = data[0: index1]
        distance1 = data[index1 + 1: index2]
        distance2 = data[index2 + 1: index3]
        distance3 = data[index3 + 1: index4]
        # print angle, distance1, distance2, distance3
        # distance3 = data[index3 + 1: len(data)]
        try:
            separated_length = map(int, angle)
        except:
            return 1
        final_lenght = 0
        for num in separated_length:
            final_lenght = final_lenght * 10
            final_lenght = final_lenght + num
        angle = final_lenght
        # print int(distance1)+4
        self.iAngle1 = int(angle)
        self.iAngle1_back = self.iAngle1
        self.iAngle2 = 180 - self.iAngle1
        self.iDistance1 = int(distance1)
        self.iDistance2 = int(distance2)
        self.iDistance3 = int(distance3)
        return 0


    def get_data(self, source):
        if source == 'serial':
            return self.process.recv(1024)
        if source == 'file':
            lin = self.fobj.readline()
            # print lin
            lin = lin.split()
            lin.insert(1, ',')
            lin.insert(3, ':')
            lin.insert(5, ';')
            lin.insert(7, '.')
            return ''.join(lin)

    def main(self):
        self.file_conn()
        # self.processing_conn()
        self.matlab_conn()
        try:
            print "try"
            while True:

                line = self.get_data('file')
                # line = self.process.recv(1024)
                print line
                if line == ',:;.':
                    if cv2.waitKey(0) == 27:
                        break
                error = self.serialEvent(line)
                if error == 1:
                    continue
                self.img = self.draw_dot1(self.img)
                self.img = self.draw_dot2(self.img)
                self.img = self.draw_dot3(self.img)
                if True:
                    self.matlab.sendall(str(self.max_val) + "\n")
                    brake = self.matlab.recv(16).split()
                    self.matlab.recv(16)
                    print brake
                    if len(brake)<2:
                        continue
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    image = self.img.copy()
                    cv2.putText(image, 'Brake=' + brake[0], (20, 27), font, 1, (0, 255, 255), 2)
                    cv2.putText(image, 'Throttle =' +brake[1], (20, 60), font, 1, (255, 0, 255), 2)
                    cv2.imshow("img", image)
                else:cv2.imshow("Image",self.img)

                if cv2.waitKey(10) == 27:
                    break
                if not line:
                    break
        finally:
            print "Closing"
            self.fobj.close()
            self.matlab.close()
            # self.process.close()


ldr = draw_lidar(9)
ldr.main()

cv2.destroyAllWindows()

# arduino = serial.Serial('COM3', 9600, timeout=.1)
# while True:
#     data = arduino.readline()  # the last bit gets rid of the new-line chars
#     if data:
#         print data
