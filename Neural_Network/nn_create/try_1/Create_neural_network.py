# from __future__ import division, print_function, absolute_import
#

from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
import tensorflow as tf
import cv2
import numpy as np
import glob
import time

print('Loading training data...')
e0 = cv2.getTickCount()

# load training data
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 2), 'float')
training_data = glob.glob('training_data_temp/*.npz')

for single_npz in training_data:
    with np.load(single_npz) as data:
        print(data.files)
        train_temp = data['train']
        test_labels_temp = data['train_labels']
        print(train_temp.shape)
        print(test_labels_temp.shape)
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, test_labels_temp))

train = image_array[1:, :]
test_labels = label_array[1:, :]
print(train.shape)
print(test_labels.shape)
e00 = cv2.getTickCount()
time0 = (e00 - e0) / cv2.getTickFrequency()
print('Loading image duration:', time0)

X = train
X = X.reshape([-1, 120, 320, 1])
Y = test_labels
# Building convolutional network
input_data1 = input_data(shape=[None, 120, 320, 1], name='input')
conv1 = conv_2d(input_data1, 32, 5, activation='relu', regularizer="L2", name="conv1")
pool1 = max_pool_2d(conv1, 2)
conv2 = conv_2d(pool1, 64, 5, activation='relu', regularizer="L2",name="conv2")
pool2 = max_pool_2d(conv1, 2)
drp1 = dropout(conv2, 0.8)
fc1 = fully_connected(drp1, 128, activation='tanh',name="fullyConnected")
drp2 = dropout(fc1, 0.8)
fc2 = fully_connected(drp2, 2, activation='softmax')
output = regression(fc2, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')
### add this "fix":
col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
for x in col:
    tf.add_to_collection(tf.GraphKeys.VARIABLES, x)

# Training
model = tflearn.DNN(output, tensorboard_verbose=3, checkpoint_path='check_point/', tensorboard_dir='tensorboard/',
                    max_checkpoints=1)
#
# model.load("checkpoint")
model.fit(X, Y, n_epoch= 1,show_metric=True)
#
# # model.save("model.tflearn")
#
# print(model.get_weights(input_data1.W), )
print (model.get_weights(conv1.W).shape,)
print (model.get_weights(conv2.W).shape),
print(model.get_weights(fc1.W).shape),
print(model.get_weights(fc2.W).shape),
print (model.get_weights(output.W).shape )
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img, (120, 320))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_re = image.reshape([-1, 120, 320, 1])
    cv2.imshow("images",image)
    print(model.predict(image_re))
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()