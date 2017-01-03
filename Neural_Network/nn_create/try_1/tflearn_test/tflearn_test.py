""" Linear Regression Example """

from __future__ import absolute_import, division, print_function

import tflearn
import tensorflow as tf

# Regression data
X = [3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167, 7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1]
Y = [1.7, 2.76, 2.09, 3.19, 1.694, 1.573, 3.366, 2.596, 2.53, 1.221, 2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3]
with tf.Graph().as_default():
    # init_op = tf.global_variables_initializer()
    # Add ops to save and restore all the variables.
    # saver = tf.train.Saver()
    # Later, launch the model, initialize the variables, do some work, save the
    # variables to disk.
    # with tf.Session() as sess:
    #     sess.run(init_op)
        #
        # Linear Regression graph
    input_ = tflearn.input_data(shape=[None])
    linear = tflearn.single_unit(input_)
    regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                    metric='R2', learning_rate=0.01)
    ### add this "fix":
    col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
    for x in col:
        tf.add_to_collection(tf.GraphKeys.VARIABLES, x)

    m = tflearn.DNN(regression,tensorboard_verbose=0, tensorboard_dir='tensorboard/')
    m.fit(X, Y, n_epoch=1000, show_metric=True, snapshot_epoch=False)

    print("\nRegression result:")
    print("Y = " + str(m.get_weights(linear.W)) +
          "*X + " + str(m.get_weights(linear.b)))

    # m.save("model.tflearn")
    # save_path = saver.save(sess, "/tmp/model.ckpt")
    # print("Model saved in file: %s" % save_path)




    W = tf.Variable(m.get_weights(linear.W))
    b = tf.Variable(m.get_weights(linear.b))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        # Initializing the variables
        init = tf.initialize_all_variables()
        # Initialize variables
        sess.run(init)




















    print("\nTest prediction for x = 3.2, 3.3, 3.4:")
    print(m.predict([3.2, 3.3, 3.4]))
    # should output (close, not exact) y = [1.5315033197402954, 1.5585315227508545, 1.5855598449707031]


# tensorboard --logdir=tensorboard