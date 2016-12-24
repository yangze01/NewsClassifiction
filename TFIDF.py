# coding=utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from Segment.MySegment import *
from optOnMysql.SegsOnMysql import *
from optOnMysql.PaperOnMongodb import *
from writeRead.WriteRead import *
article_unit = dict()
import math

class TFIDF(object):
    def __init__(self):
        self.name = "count"
    def TF_IDF(self,seg_iter):
        opt_rw = WriteRead("C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\myidf.json")
        idf = opt_rw.get_json_data()

        word_count = {
            "_id":"",
            "tf_idf":{}
        }
        word_count["_id"] = seg_iter[0]
        word_list = seg_iter[1].split(',')
        wordnum = len(word_list)
        for word in word_list:
            if word in word_count["tf_idf"]:
                word_count["tf_idf"][word] = word_count["tf_idf"][word] + 1/wordnum*idf[word]
            else:
                word_count["tf_idf"][word] = 1/wordnum*idf[word]
        # print(word_count)
        return word_count

    def IDF(self,seg_iter):
        Idf_Count = dict()
        art_num = len(seg_iter)
        i = 0
        for word_iter in seg_iter:
            
            # print("++++++++++"+str(i)+"+++++++++++++++")
            print(i)
            word_set = set(word_iter[1].split(','))
            # print("word_set_len: "+str(len(word_set)))
            for word in word_set:
                # print("in word")
                # print(word)
                if word in Idf_Count:
                    Idf_Count[word] = Idf_Count[word] + 1#/(art_num + 1)
                else:
                    Idf_Count[word] = 1#/(art_num + 1)
            i = i + 1
        print("the idf_count: " + str(len(Idf_Count)))
        for k,v in Idf_Count.items():
            Idf_Count[k] = math.log(art_num/(v+1))
            # print(k)
            # print(Idf_Count[k])
        return Idf_Count
            # print(v)
        # opt.connClose()
if __name__ == "__main__":
    # word_count = {
    #     '_id':"",
    #     "tf_count":{}
    # }
    # word_list = ['a','b','c','a','b','c','c','a','d']

    db_uri = "mongodb://root:1234@localhost:27017/?authSource=paper"
    db_name = "paper"
    xlient = MongoClient(db_uri)
    db = xlient[db_name]
    opt_mongo = PaperOnMongo()
    opt_mongo.connect2Mongo(db_uri,db_name)
    opt_rw = WriteRead("\jsonfile\\myidf.json")


    opt_tfidf = TFIDF()
    opt = SegsOnMysql()
    seg_iter = opt.findall()[0:]

    i = 0
    for iteriter in seg_iter:
        print(i)
        opt_tfidf.TF_IDF(iteriter)
        i = i + 1

    opt.connClose()
