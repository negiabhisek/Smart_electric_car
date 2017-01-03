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


def load_data():
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
    return train,test_labels

def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME')


# Create model
def conv_net(x, weights, biases, dropout):
    # # Reshape input picture
    # x = tf.reshape(x, shape=[-1, 28, 28, 1])

    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Max Pooling (down-sampling)
    conv1 = maxpool2d(conv1, k=2)

    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Max Pooling (down-sampling)
    conv2 = maxpool2d(conv2, k=2)

    # Fully connected layer
    # Reshape conv2 output to fit fully connected layer input
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tflearn.dropout(fc1, 0.8)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Parameters
learning_rate = 0.01
training_epochs = 2
training_iters = 200000
batch_size = 1
n_input = 38400
n_classes = 2 # MNIST total classes (0-9 digits)
dropout_val = 0.75 # Dropout, probability to keep units

train,test_labels = load_data()
X_train = train
Y_train = test_labels
print (X_train.shape)
print (Y_train.shape)
# tf.reset_default_graph()
# g = tf.Graph()
with tf.Graph().as_default():

    X = tf.placeholder(shape=(None, 38400), dtype=tf.float32)
    Y = tf.placeholder(shape=(None, 2), dtype=tf.float32)
    keep_prob = tf.placeholder(tf.float32)  # dropout (keep probability)
    # keep_prob = tf.placeholder(tf.float32)  # dropout (keep probability)
    # input_data1 = tf.reshape(X, [-1, 120, 320, 1])

    # Building convolutional network
    # input_data1 = input_data(shape=[None, 120, 320, 1], name='input')
    # conv1_w = init_weights([3, 3, 1, 32])  # 3x3x1 conv, 32 outputs
    # conv1 = conv_2d(X, 32, 5, activation='relu', regularizer="L2", name="conv1")
    # pool1 = max_pool_2d(conv1, 2)
    # conv2 = conv_2d(pool1, 64, 5, activation='relu', regularizer="L2",name="conv2")
    # pool2 = dropout(conv2, 0.8)
    # fc1 = fully_connected(pool2, 2, activation='softmax',name="fullyConnected")

    # Create some wrappers for simplicity

    weights = {
        # 5x5 conv, 1 input, 32 outputs
        'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
        # 5x5 conv, 32 inputs, 64 outputs
        'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
        # fully connected, 7*7*64 inputs, 1024 outputs
        'wd1': tf.Variable(tf.random_normal([8 * 8 * 64, 1024])),
        # 1024 inputs, 10 outputs (class prediction)
        'out': tf.Variable(tf.random_normal([1024, n_classes]))
    }

    biases = {
        'bc1': tf.Variable(tf.random_normal([32])),
        'bc2': tf.Variable(tf.random_normal([64])),
        'bd1': tf.Variable(tf.random_normal([1024])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }

    pred = conv_net(X, weights, biases, keep_prob)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initializing the variables
    init = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init)
        step = 1
        # Keep training until reach max iterations

        for epoch in range(training_epochs):
            avg_cost = 0.

            for i in range(len(Y_train)):
                batch_x=X_train[i]
                batch_y = Y_train[i]
                # Run optimization op (backprop)
                _, c = sess.run(optimizer, feed_dict={X: batch_x, Y: batch_y,
                                               keep_prob: dropout})
                # Compute average loss
                avg_cost += c / len(Y_train)
            if step % 1 == 0:
                # Calculate batch loss and accuracy
                loss, acc = sess.run([cost, accuracy], feed_dict={X: X_train,
                                                                  Y: Y_train,
                                                                  keep_prob: 1.})
                print("Iter " + str(step * batch_size) + ", Minibatch Loss= " + \
                      "{:.6f}".format(loss) + ", Training Accuracy= " + \
                      "{:.5f}".format(acc))
            step += 1
        print("Optimization Finished!")

        # Calculate accuracy for 256 mnist test images
        print("Testing Accuracy:", \
              sess.run(accuracy, feed_dict={X: X_train,
                                            Y: Y_train,
                                            keep_prob: 1.}))
