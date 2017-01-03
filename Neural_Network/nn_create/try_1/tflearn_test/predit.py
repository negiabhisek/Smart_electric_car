""" Linear Regression Example """

from __future__ import absolute_import, division, print_function

import tflearn
import tensorflow as tf


with tf.Graph().as_default():
    # Add an op to initialize the variables.
    init_op = tf.global_variables_initializer()
    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()
    # Later, launch the model, initialize the variables, do some work, save the
    # variables to disk.
    with tf.Session() as sess:
        sess.run(init_op)
        # Do some work with the model.


        # Linear Regression graph
        input_ = tflearn.input_data(shape=[None])
        linear = tflearn.single_unit(input_)
        regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                        metric='R2', learning_rate=0.01)
        ### add this "fix":
        col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
        for x in col:
            tf.add_to_collection(tf.GraphKeys.VARIABLES, x)

        m = tflearn.DNN(regression)

        # m.load("model.tflearn")
        print("\nTest prediction for x = 3.2, 3.3, 3.4:")
        print(m.predict([3.2, 3.3, 3.4]))
        # should output (close, not exact) y = [1.5315033197402954, 1.5585315227508545, 1.5855598449707031]