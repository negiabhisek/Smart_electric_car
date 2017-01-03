'''
A Convolutional Network implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
import cv2
import numpy as np
import glob

#import data
class datashape:
    def __init__(self):
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples = 0
        self.load_data()

    def load_data(self):
        print('Loading training data...')
        e0 = cv2.getTickCount()

        # load training data
        image_array = np.zeros((1, 9600))
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
        # return train,test_labels
        self._images = train
        self._labels = test_labels
        self._num_examples = len(test_labels)

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            # assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]

# Parameters
learning_rate = 0.001
training_iters = 3000
batch_size = 128
display_step = 10

# Network Parameters
n_input = 9600 # MNIST data input (img shape: 28*28)
n_classes = 2 # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units
model_path = "/tmp/model.ckpt"

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)
mnist = datashape()

# Create some wrappers for simplicity
def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME')


# Create model
def conv_net(x, weights, biases, dropout):
    # Reshape input picture
    x = tf.reshape(x, shape=[-1, 120, 80, 1])

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
    fc1 = tf.nn.dropout(fc1, dropout)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Store layers weight & bias
weights = {
    # 5x5 conv, 1 input, 32 outputs
    'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
    # 5x5 conv, 32 inputs, 64 outputs
    'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
    # fully connected, 7*7*64 inputs, 1024 outputs
    'wd1': tf.Variable(tf.random_normal([30*20*64, 800])),
    # 1024 inputs, 10 outputs (class prediction)
    'out': tf.Variable(tf.random_normal([800, n_classes]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([32])),
    'bc2': tf.Variable(tf.random_normal([64])),
    'bd1': tf.Variable(tf.random_normal([800])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}
print('Training the Network...')
e0 = cv2.getTickCount()

# Construct model
pred = conv_net(x, weights, biases, keep_prob)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()
saver = tf.train.Saver()

# Launch the graph
with tf.Session() as sess:
    save_path = saver.restore(sess, model_path)
    print("Model restored from file: %s" % save_path)
    sess.run(init)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        e0 = cv2.getTickCount()
        ret, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(img, (120, 80))

        image_array = image.reshape(-1,9600)
        # print (image_array.shape)
        image_re = image_array.reshape([-1, 120, 80, 1])
        cv2.imshow("images", image)
        predict_op = tf.argmax(pred, 1)
        feed_dict = {x: image.reshape(1, 9600),
                     keep_prob: 1.}
        # cv2.imshow("image", mnist._images[t].reshape(28, 28))
        classification = sess.run(predict_op, feed_dict)
        if classification == 0:
            print ("on the screen\tTime = "+ str((cv2.getTickCount()-e0)/cv2.getTickFrequency()))
        else:
            print ("not on the screen\tTime = "+ str((cv2.getTickCount()-e0)/cv2.getTickFrequency()))
        #print(classification)
        # print(model.predict(image_re))
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
