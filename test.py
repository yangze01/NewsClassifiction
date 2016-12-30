# coding=utf-8
from __future__ import division
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import gensim
import data_helpers
from textcnnModel import TextCNN
from tensorflow.contrib import learn
import sys
import json
reload(sys)
BasePath = sys.path[0]

# print(BasePath)
# logging.getLogger().setLevel(logging.INFO)

def get_json_data(userdir):
    readf = open(userdir,'r')
    json_data = readf.read()
    readf.close()
    decode_json = json.loads(json_data)
    return decode_json

def save2json(userdir,data2save):
    encode_json = json.dumps(data2save)
    writef = open(userdir,'w')
    writef.write(encode_json)
    writef.close()

if __name__ == "__main__":
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



############################################################################
    # test_tf = tf.random_uniform([10,300], -1.0, 1.0)
    # # test_zeros = tf.zeros([300])
    # print("________________________test_tf___________________________")
    # print(test_tf[0])
    # sess = tf.Session()
    # print(len(sess.run(test_tf[0])))
    #
    # a = list(np.zeros(300,dtype='float32'))
    # # print(a)
    # IdVec.append(a)
    # tmp = tf.constant(IdVec)
    # print(len(sess.run(tmp[0])))
    # # sess = tf.Session()
    # # print sess.run(tmp)
############################################################################

    FileIdVec = BasePath + "/jsonfile/IdVec"
    IdVec = list()
    # print(IdVec)
    # print(model[vocab_processor.vocabulary_.reverse(1)].dtype)
    for id in range(1,len(vocab_processor.vocabulary_)):
        print(id)
        IdVec.append(list(model[vocab_processor.vocabulary_.reverse(id)]))
    sess = tf.Session()
    tmp = tf.constant(IdVec)
    print(len(sess.run(tmp[0])))
    print sess.run(tmp[0])





    # a = {
    #         "_id" : {
    #                     "$oid" : "57fd0e9c0d00f0458ea0b372"
    #                 },
    #         "title" : "基于FPGA的Turbo码译码算法实现",
    #         "journal" : "系统工程与电子技术",
    #         "quote" : "11",
    #         "abstract" : {
    #                         "Chinese" : "在分析Turbo码编译码中MAP类译码算法的基础上,重点研究了Max-Log-MAP译码算法的工程实现方法.为解决Turbo码译码嚣FPGA实现时的复杂性高、存储量大的问题,提出了一种基于FPGA的优化译码器结构和译码算法实现方案,有效减少了存储容量,提高了处理速度,并在Altera的EP2S90芯片上实现了10MHz速率的Turbo码译码器,通过时序仿真验证了译码结构的有效性.",
    #                         "English" : ""
    #                       },
    #         "date" : {
    #                     "period" : "8",
    #                     "year" : "2008"
    #                  },
    #         "link" : "http://d.wanfangdata.com.cn/Periodical/xtgcydzjs200808046",
    #         "authors" : {
    #                         "桑会平" : {
    #                                         "institution" : "电子科技集团54所",
    #                                         "location" : "石家庄"
    #                                    },
    #                         "张桂华" : {
    #                                         "institution" : "西安电子科技大学电子工程学院",
    #                                         "location" : "西安"
    #                                    },
    #                         "姬红兵" : {
    #                                         "institution" : "电子科技集团54所",
    #                                         "location" : "石家庄"
    #                                    }
    #                     },
    #         "keywords" : [ "Turbo码", "Max-Log-MAP算法", "FPGA", "译码器" ],
    #         "include" : "ISTIC",
    #         "institutions" : {
    #                                 "电子科技集团54所" : "石家庄",
    #                                 "西安电子科技大学电子工程学院" : "西安"
    #                          }
    #         }
    # print(math.log(6.75310642896e-05))
