# coding=utf-8
import logging
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import json
import gensim
from numpy import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
def train():
    corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\courpus.json"
    id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\id_list.json"
    fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\mymodel"
    sentences = get_json_data(corpus_file)[0:]
    id_list = get_json_data(id_file)[0:]
    model = gensim.models.Word2Vec(sentences, size=400, window=5, min_count=1, workers=20)
    print("complete train")
    model.save(fname)
    print("model reload")
def load_model():
    fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\mymodel"
    model = gensim.models.Word2Vec.load(fname)
    return model


if __name__ == "__main__":
    corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\courpus.json"
    id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\id_list.json"
    cate_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\cate_list.json"
    feature_list = list()
    cate_dict = {'股市':1,'财经':2,'国际':3,'科技':4,'军事':5,'社会':6,'体育':7,'国内':8,'美股':9,'娱乐':10,'娱乐':11,'其他':12}
    model = load_model()
    print(type(model["美股".decode('utf8')]))
    f = open('C:\Users\john\Desktop\spider\NewsClassifiction\\test.txt','w')
    sentences = get_json_data(corpus_file)[10000:]
    cates = get_json_data(cate_file)[10000:]
    i = 0
    for sentence in sentences:
        len_word = len(set(sentence))
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(i)
        # print(cates[i])
        # print(' '.join(sentence))
        # print("the len of sentence is : " + str(len_word))
        tmp_num = zeros(400)
        for word in set(sentence):
            tmp_num = tmp_num + model[word.decode('utf8')]
        tmp_num = tmp_num/len_word
        svm_num = str(cate_dict[cates[i].encode('utf8')])+' '+' '.join([str(svm_i+1) + ':' + str(tmp_num.tolist()[svm_i]) for svm_i in range(len(tmp_num.tolist()))])
        print(svm_num)
        f.write(svm_num)
        f.write("\n")
        # feature_list.append(tmp_num.tolist())
        i = i + 1
    f.close()
