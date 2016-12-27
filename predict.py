# coding=utf-8
import os
import sys
reload(sys)
import time
import json
import cPickle
import datetime
import numpy as np
import data_helpers
import tensorflow as tf
import tensorlayer as  tl
sys.setdefaultencoding('utf8')

from textcnnModel import Model
from tensorflow.contrib import learn
import sys
BasePath = sys.path[0]

# Parameters
# ==================================================

# Data Parameters
# tf.flags.DEFINE_string("positive_data_file", BasePath + "/data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
# tf.flags.DEFINE_string("negative_data_file", BasePath + "/data/rt-polaritydata/rt-polarity.neg", "Data source for the positive data.")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", BasePath + "/runs/1482667968/checkpoint", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# CHANGE THIS: Load data. Load your own data here
# if FLAGS.eval_train:
    # x_raw, y_test = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)
    # y_test = np.argmax(y_test, axis=1)
#
# else:
#     x_raw = ["a masterpiece four years in the making", "everything is off."]
#     y_test = [1, 0]
# print("\nEvaluating...\n")

# x_test, y_test = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)
# y_test = np.argmax(y_test, axis=1)
x_test,y = data_helpers.get_predict_data()


# Evaluation
# ==================================================
checkpoint_file = BasePath + "/runs/1482667968/checkpoints/model-42800"#tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
print("!)@#(#&@&#*$(#()!@#$#*@&#")
print(checkpoint_file)
graph = tf.Graph()
with tf.Graph().as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        print(input_x)
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
        # dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]

        # Generate batches for one epoch
        batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

        # Collect the predictions here
        all_predictions = []

        for x_test_batch in batches:
            batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
            all_predictions = np.concatenate([all_predictions, batch_predictions])
# Print accuracy if y_test is defined
if y_test is not None:
    correct_predictions = float(sum(all_predictions == y_test))
    print("Total number of test examples: {}".format(len(y_test)))
    print("Accuracy: {:g}".format(correct_predictions/float(len(y_test))))

# Save the evaluation to a csv
predictions_human_readable = np.column_stack((np.array(x_raw), all_predictions))
print(predictions_human_readable)



# if __name__ =="__main__":
#     FLAGS = tf.flags.FLAGS
#     FLAGS._parse_flags()
#     print("\nParameters:")
#     for attr, value in sorted(FLAGS.__flags.items()):
#         print("{}={}".format(attr.upper(), value))
#     print("")
