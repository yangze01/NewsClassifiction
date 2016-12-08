# coding=utf-8
import sys
reload(sys)
from Segment.MySegment import *
from optOnMysql.SegsOnMysql import *
sys.setdefaultencoding('utf8')
if __name__ == "__main__":
    myseg = MySegment()
    opt_news = NewsOnMysql()
    opt_segs = SegsOnMysql()

    paraph_list = opt_news.findall()[0:4]
    i = 0
    for new_tuple in paraph_list:
        print(i)
        sen_list = myseg.paraph2sen(new_tuple[2])
        wordlist = myseg.senlist2word(sen_list)
        # print(wordlist)
        word2save = ','.join(wordlist)
        print("#########word2save##########")
        print(word2save)

        i = i + 1
        print("#######################")
    myseg.close()
    opt_news.connClose()
    opt_segs.connClose()

    # segsunit = SegsUnit().segs_unit
    # segsunit["_id"] = "test"
    # segsunit["segments"] = "一,二,三,四,五,六,七,八"
    # print(segsunit)
    # opt_segs = SegsOnMysql()
    # opt_segs.insertOneSegs(segsunit)
    # a = opt_segs.findall()
    # for i in a:
    #     print(i[1].split(','))
    # opt_segs.connClose()




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
