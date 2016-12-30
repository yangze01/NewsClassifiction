import tensorflow as tf
import numpy as np
import data_helpers
import json
import os
import time
import datetime
import gensim
import data_helpers
import sys
reload(sys)
BasePath = sys.path[0]
from tensorflow.contrib import learn

def get_json_data(userdir):
    readf = open(userdir,'r')
    json_data = readf.read()
    readf.close()
    decode_json = json.loads(json_data)
    return decode_json

class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """
    def __init__(
      self, sequence_length, num_classes, vocab_size,
      embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):

        # Placeholders for input, output and dropout

        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)
############################################################################
        # Load data
        print("Loading data...")
        x_text, y = data_helpers.load_data_and_labels()

        # Build vocabulary
        max_document_length = max([len(x.split(" ")) for x in x_text])
        print("~_~$!$@^&!*~!$%~^~&!*@(((~!~^%!^~!%^~%~^~%)))")
        print("max_document_length is :")
        print(max_document_length)
        vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
        x = np.array(list(vocab_processor.fit_transform(x_text)))
        print(x[1])
        title_fname = BasePath + "/jsonfile/title_Word2Vec"
        model = gensim.models.Word2Vec.load(title_fname)

        FileIdVec = BasePath + "/jsonfile/IdVec"
        IdVec = list()
        # print(IdVec)
        # print(model[vocab_processor.vocabulary_.reverse(1)].dtype)
        zeros_indict = list(np.zeros(300,dtype='float32'))
        IdVec.append(zeros_indict)
        for id in range(1,len(vocab_processor.vocabulary_)):
            print(id)
            IdVec.append(list(model[vocab_processor.vocabulary_.reverse(id)]))
        sess = tf.Session()
        tmp = tf.constant(IdVec)

############################################################################

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            W = tf.Variable(
                #tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                tmp,
                name="W")
            # print(vocab_size)
            # print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            # print(a[0])
            self.embedded_chars = tf.nn.embedding_lookup(W, self.input_x)
            self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution Layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                    self.embedded_chars_expanded,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")
                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(3, pooled_outputs)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

        # Add dropout
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)

        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # CalculateMean cross-entropy loss
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(self.scores, self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
