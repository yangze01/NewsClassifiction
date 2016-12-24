# coding=utf-8
# from __future__ import division
import sys
reload(sys)
import json
import string
import os
from optOnMysql.SegsOnMysql import *
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
sys.setdefaultencoding('utf8')
import math
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
class TFIDF(object):
    def __init__(self):
        self.name = "count"

if __name__ == "__main__":
    # corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\courpus.json"
    # id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\id_list.json"
    # corpus1 = get_json_data(corpus_file)[0:3000]
    # id_list = get_json_data(id_file)
    # i = 0
    # corpus = list()
    # for sentence in corpus1:
    #     print(i)
    #     corpus.append(' '.join(sentence).encode('utf8'))
    #     i = i + 1
    # # print(corpus)
    #
    # vectorizer = CountVectorizer()#该类会将文本中的词语转换为词频矩阵
    # transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
    # tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    # # # # # print(tfidf)
    # word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    # print(len(word))
    #
    # weight = tfidf.toarray()

    # sFilePath = 'C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\tfidffile'
    # if not os.path.exists(sFilePath) :
    #     os.mkdir(sFilePath)
    # for i in range(len(weight)):
    #     print(u"--------Writing all the tf-idf in the",i,u" file into ",sFilePath+'\\'+id_list[i]+'.txt',"--------")
    #     f = open(sFilePath+'\\'+id_list[i]+'.txt','w+')
    #     for j in range(len(word)):
    #         print("+++word++++")
    #         print(word[j])
    #         print("+++weight++++")
    #         print(weight[i][j])
    #         print("_____tfidf_____")
    #         print(tfidf[i])
    #         f.write(word[j]+"    "+str(weight[i][j])+"\n")
    #     f.close()





    # weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    # for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #     print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"
    #     for j in range(len(word)):
    #         print word[j],weight[i][j]
