from sklearn.datasets import load_diabetes
import tensorflow as tf
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

dataset = load_diabetes()
x_data = dataset.data
y_data = dataset.target

y_data = y_data.reshape(442, 1)

print(x_data.shape, y_data.shape)   # (442, 10) (442, 1)

x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.2, random_state=66
)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

x = tf.placeholder(tf.float32, shape=[None, 10])
y = tf.placeholder(tf.float32, shape=[None, 1])

# [실습] 맹그러!!!

w = tf.Variable(tf.random_normal([10, 1], name='weight'))
b = tf.Variable(tf.random_normal([1], name='bias'))

hypothesis = tf.matmul(x, w) + b

cost = tf.reduce_mean(tf.square(hypothesis - y))

train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())

    for step in range(6001):
        cost_val, _ = sess.run([cost, train], feed_dict = {x:x_train, y:y_train})

        if step % 50 == 0:
            print(step, "\n", "loss : ", cost_val)

    print('R2 : ', r2_score(y_test, sess.run(hypothesis, feed_dict={x:x_test})))

# R2 :  0.5050776322665333    