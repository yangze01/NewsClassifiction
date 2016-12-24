# coding=utf-8
import sys
import tensorflow as tf
reload(sys)
sys.setdefaultencoding('utf8')
if __name__ == "__main__":
    hello = tf.constant('Hello World!')
    sess = tf.Session()
    print("++++++++++++++++++++++++")
    sess.run(hello)
    a = tf.constant(10)
    b = tf.constant(32)
    sess.run(a+b)
