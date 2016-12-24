# coding=utf-8
import sys
reload(sys)
import json
sys.setdefaultencoding('utf8')
from Segment.MySegment import *
from optOnMysql.SegsOnMysql import *

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

def segMain(i):
    segsunit = SegsUnit().segs_unit
    myseg = MySegment()
    opt_news = NewsOnMysql()
    opt_segs = SegsOnMysql()

    paraph_list = opt_news.findall()[i:]
    i = 0
    for new_tuple in paraph_list:
        print(i)
        # print(new_tuple[1])
        # print("the id will be segment:" + str(new_tuple[0]))
        segsunit["category"] = new_tuple[4].encode('utf8')
        segsunit["_id"] = new_tuple[0].encode("utf8")
        title_list = myseg.paraph2sen(new_tuple[1])
        title_wordlist = myseg.senlist2word(title_list)
        segsunit["segtitle"] = ','.join(title_wordlist).encode("utf8")
        sen_list = myseg.paraph2sen(new_tuple[2])
        wordlist = myseg.senlist2word(sen_list)
        segsunit["segments"] = ','.join(wordlist).encode("utf8")
        opt_segs.insertOneSegs(segsunit)
        i = i + 1
    myseg.close()
    opt_news.connClose()
    opt_segs.connClose()

def save2file():
    corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\courpus.json"
    id_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\id_list.json"
    cate_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\cate_list.json"
    title_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\title_courpus.json"
    corpus = list()
    id_list = list()
    cate_list = list()
    title_courpus_list = list()
    opt = SegsOnMysql()
    seg_iter = opt.findall()[0:]
    i = 0
    for seg_seg in seg_iter:
        print(i)
        # print(seg_seg[2])
        title_courpus_list.append(seg_seg[2].encode('utf8').split(','))
        # id_list.append(seg_seg[0])
        corpus.append(seg_seg[1].encode('utf8').split(','))
        # cate_list.append(seg_seg[3])
        i = i + 1
    opt.connClose()
    # print(cate_list)
    save2json(title_file,title_courpus_list)
    # save2json(cate_file,cate_list)
    save2json(corpus_file,corpus)
    # save2json(id_file,id_list)
    # corpus = get_json_data(corpus_file)
    # print(corpus[9])

if __name__ == "__main__":
    save2file()
    # segMain(0)
    # title_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\title_courpus.json"
    # a = get_json_data(title_file)[0]
    # print(a)
    # corpus_file = "C:\Users\john\Desktop\spider\NewsClassifiction\jsonfile\\courpus.json"
    # a = get_json_data(corpus_file)[0]
    # print(a)
