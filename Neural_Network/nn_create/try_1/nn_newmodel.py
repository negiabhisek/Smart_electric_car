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
network = input_data(shape=[None, 120, 320, 1], name='input')
network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = fully_connected(network, 128, activation='sigmoid')
network = dropout(network, 0.8)
# network = fully_connected(network, 256, activation='relu')
# network = dropout(network, 0.8)
network = fully_connected(network, 2, activation='softmax')
output = regression(network, optimizer='adam', learning_rate=0.01,
                    loss='categorical_crossentropy', name='target')
### add this "fix":
col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
for x in col:
    tf.add_to_collection(tf.GraphKeys.VARIABLES, x)

# Training
model = tflearn.DNN(output, tensorboard_verbose=3, tensorboard_dir='tensorboard/')
#
# model.load("checkpoint")
model.fit({'input': X}, {'target': Y}, n_epoch=2,
          snapshot_step=100, show_metric=True, run_id='convnet_mnist')
#
# # model.save("model.tflearn")
#
# print(model.get_weights(input_data1.W), )
# print (model.get_weights(conv1.W).shape,)
# print (model.get_weights(conv2.W).shape),
# print(model.get_weights(fc1.W).shape),
# print(model.get_weights(fc2.W).shape),
# print (model.get_weights(output.W).shape )
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img, (320, 120))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_array = image.reshape(1, 38400)
    image_re = temp_array.reshape([-1, 120, 320, 1])
    cv2.imshow("images", image)
    print(model.predict(image_re))
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
