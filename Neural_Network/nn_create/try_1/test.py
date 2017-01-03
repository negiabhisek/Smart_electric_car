from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
import tensorflow as tf
import cv2
import numpy as np
import glob
with tf.Graph().as_default():
    # Building convolutional network
    network = input_data(shape=[None, 120, 320, 1], name='input')
    network = conv_2d(network, 32, 5, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = conv_2d(network, 64, 5, activation='relu', regularizer="L2")
    network = dropout(network, 0.8)
    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='target')
    ### add this "fix":
    col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
    for x in col:
        tf.add_to_collection(tf.GraphKeys.VARIABLES, x)

    # Training
    model = tflearn.DNN(network, tensorboard_verbose=3, checkpoint_path='model_ba.ckpt',
                        max_checkpoints=1)
    model.load("model.tflearn")
    img = cv2.imread("train2.jpg")
    img = cv2.resize(img, (320, 120))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = image.reshape([-1, 120, 320, 1])
    print (model.predict(image))
