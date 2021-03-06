import tensorflow as tf
import numpy as np
tf.set_random_seed(66)

x_data = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=np.float32)
y_data = np.array([[0], [1], [1], [0]], dtype=np.float32)

# [7분이면 충분하겠지] 맹그러봐

x = tf.placeholder(tf.float32, shape=[None, 2])
y = tf.placeholder(tf.float32, shape=[None, 1])

w1 = tf.Variable(tf.random_normal([2, 100], name='weight'))
b1 = tf.Variable(tf.random_normal([100], name='bias'))
layer1 = tf.sigmoid(tf.matmul(x, w1) + b1) # sigmoid로 변환
# model.add(Dense(100, input_dim=2, activation='sigmoid))

w2 = tf.Variable(tf.random_normal([100, 70]), name='weight2')
b2 = tf.Variable(tf.random_normal([70]), name='bias2')
layer2 = tf.sigmoid(tf.matmul(layer1, w2) + b2) # sigmoid로 변환
# model.add(Dense(70, activation='sigmoid))

w3 = tf.Variable(tf.random_normal([70, 1]), name='weight3')
b3 = tf.Variable(tf.random_normal([1]), name='bias3')
hypothesis = tf.sigmoid(tf.matmul(layer2, w3) + b3) # sigmoid로 변환
# model.add(Dense(1, activation='sigmoid))

# cost = tf.reduce_mean(tf.square(hypothesis - y))
cost = -tf.reduce_mean(y*tf.log(hypothesis)+(1-y)*tf.log(1-hypothesis)) # loss = binary_crossentropy로 변환

train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, y), dtype=tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(5001):
        cost_val, _ = sess.run([cost, train], feed_dict={x:x_data, y:y_data})

        if step % 200 == 0:
            print(step, cost_val)

    h, c, a = sess.run([hypothesis, predicted, accuracy],
                        feed_dict ={x:x_data, y:y_data})
    print(" 예측 값 : ", '\n', h, '\n', "원래 값 : ", '\n', c, '\n', "Accuracy : ", a)

#  예측 값 :  
#  [[0.03914018]
#  [0.95837146]
#  [0.9677183 ]
#  [0.03522458]]
#  원래 값 :
#  [[0.]
#  [1.]
#  [1.]
#  [0.]]
#  Accuracy :  1.0