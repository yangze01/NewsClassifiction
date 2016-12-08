# coding=utf-8
import sys
from pyltp import *
from optOnMysql.NewsOnMysql import *
import re
import string
reload(sys)
sys.setdefaultencoding('utf8')

class MySegment(object):
    def __init__(self):
        self.model = 'C:\Users\john\Desktop\spider\ltp_data\cws.model'
        self.lexicon = 'lexi.model'
        self.segmentor = Segmentor()
        self.segmentor.load(self.model)

    def load_default_model(self):
        self.segmentor.load(self.model)

    def sen2word(self,sen):

        nonsentence = self.remove_punctuation(sen.decode('utf8'))
        word_obj = self.segmentor.segment(nonsentence)
        # for i in word_obj:
            # print(i)
        word_list = list(word_obj)
        return word_list

    def senlist2word(self,sentence_list):
        '''
            input:
                sentent the sen to be seg
            output:
                the word list
        '''
        word_list = list()

        for sentence in sentence_list:
            word_obj = self.sen2word(sentence)
            word_list = word_list + word_obj
        return word_list

    def paraph2sen(self,paraph):
        # print(paraph)
        sentence_obj = SentenceSplitter.split(paraph.encode('utf8'))
        sentence_list = list(sentence_obj)
        # print(sentence_list)
        return list(sentence_list)

    def remove_punctuation(self,sentence):
        return ''.join(re.findall(u'[\u4e00-\u9fff]+', sentence)).encode('utf8')
    def close(self):
        self.segmentor.release()
        print(self.segmentor.release())

if __name__ == "__main__":


    myseg = MySegment()
    opt_news = NewsOnMysql()
    # opt_mysql = OptOnMysql()
    paraph_list = opt_news.findall()[1:10]
    i = 0
    for new_tuple in paraph_list:
        print(i)
        sen_list = myseg.paraph2sen(new_tuple[2])
        wordlist = myseg.senlist2word(sen_list)
        print(','.join(wordlist))
        string.split(',')
        i = i + 1
    myseg.close()
    opt_news.connClose()
    # opt_mysql.connClose()
    # opt_news = NewsOnMysql()
    # a = opt_news.findById("010525548590.shtml")
    # # print(a[2])
    # a = myseg.paraph2sen(a[2])
    # b = myseg.senlist2word(a)
    # c= ','.join(b)
    # print(c)

    # sentencelist = myseg.paraph2sen(paraph_list[1][2])
    # wordlist = myseg.sen2word(sentencelist)
    # print(str(wordlist))
    # opt_mysql.exeUpdate("insert into segs (_id,segments) values ('"+paraph[1][0]+"','"+str(wordlist)+"')")
