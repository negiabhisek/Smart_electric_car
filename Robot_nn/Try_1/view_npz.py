__author__ = 'Abhisek Negi'

import cv2
import numpy as np
import glob

print 'Loading training data...'
e0 = cv2.getTickCount()

# load training data
image_array = np.zeros((1, 9600))
label_array = np.zeros((1, 4))
training_data = glob.glob('training_data_temp/*.npz')

for single_npz in training_data:
    with np.load(single_npz) as data:
        print data.files
        train_temp = data['train']
        label_temp = data['train_labels']
        print train_temp.shape,label_temp.shape
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, label_temp))

train = image_array[1:, :]
label = label_array[1:, :]
print train.shape,label.shape
e00 = cv2.getTickCount()
time0 = (e00 - e0) / cv2.getTickFrequency()
print 'Loading image duration:', time0

# set start time
e1 = cv2.getTickCount()

count = 0
for i in range(len(train)):
    count = count + 1
    img = train[i].reshape(80, 120)
    print count, label[i  ]

    cv2.imwrite(str(count) + ".jpg", img)
    t = cv2.imread(str(count) + ".jpg")
    cv2.imshow("image", t)
    k = cv2.waitKey(0) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
