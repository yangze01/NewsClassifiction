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
    title_courpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\title_courpus.json"
    id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\id_list.json"
    fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\Word2Vec"
    title_fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\title_Word2Vec"
    sentences = get_json_data(corpus_file)[0:]
    title_sentences = get_json_data(title_courpus_file)
    id_list = get_json_data(id_file)[0:]
    model = gensim.models.Word2Vec(title_sentences, size=300, window=5, min_count=1, workers=20)
    model1 = gensim.models.Word2Vec(title_sentences, size=300, window=5, min_count=1, workers=20)
    print("complete train")
    model.save(fname)
    model.save(title_fname)
    print("model reload")
def load_model():
    fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\Word2Vec"
    title_fname = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\title_Word2Vec"
    model = gensim.models.Word2Vec.load(fname)
    return model


if __name__ == "__main__":
    train()
    # corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\courpus.json"
    # id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\id_list.json"
    # cate_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\cate_list.json"
    # feature_list = list()
    # cate_dict = {'股市':0,'财经':1,'国际':2,'科技':3,'军事':4,'社会':5,'体育':6,'国内':7,'美股':8,'娱乐':9,'娱乐':10,'其他':11}
    # model = load_model()
    # print(type(model["美股".decode('utf8')]))
    # f = open('C:\Users\john\Desktop\spider\NewsClassifiction\\train.txt','w')
    # sentences = get_json_data(corpus_file)[:10000]
    # cates = get_json_data(cate_file)[:10000]
    # i = 0
    # for sentence in sentences:
    #     len_word = len(set(sentence))
    #     # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     print(i)
    #     # print(cates[i])
    #     # print(' '.join(sentence))
    #     # print("the len of sentence is : " + str(len_word))
    #     tmp_num = zeros(300)
    #     for word in set(sentence):
    #         tmp_num = tmp_num + model[word.decode('utf8')]
    #     tmp_num = tmp_num/len_word
    #     svm_num = str(cate_dict[cates[i].encode('utf8')])+' '+' '.join([str(svm_i+1) + ':' + str(tmp_num.tolist()[svm_i]) for svm_i in range(len(tmp_num.tolist()))])
    #     # print(svm_num)
    #     f.write(svm_num)
    #     f.write("\n")
    #     # feature_list.append(tmp_num.tolist())
    #     i = i + 1
    # f.close()
