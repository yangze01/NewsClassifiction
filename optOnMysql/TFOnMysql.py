#coding=utf-8
import pymysql
from optOnMysql import *
from SegsUnit import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class SegsOnMysql(object):
    def __init__(self):
        self.opt_OnMySql = OptOnMysql()

    def findById(self,id):
        cur = self.opt_OnMySql.exeQuery("select * from segs where _id = '"+id+"'")
        it = cur.fetchone()
        # print(it)
        if it == None:
            print("there is nothing found in seg table")
            return 0
        else:
            print(it)
            return 1

    def findall(self):
        cur = self.opt_OnMySql.exeQuery("select * from segs")
        it = cur.fetchall()
        # print(it)
        if not it:
            print("this is no data in segs")
            return it
        else:
            print("fetch all data in segs")
            return it

    def insertOneSegs(self,segs_unit):
        '''
            description:
                 insert one news into mysql
            input:
                news_unit:
                    dict of news to be inserted
            output:
                num of insert news
        '''
        # self.opt.db_user_unit.news_unit = news_unit
        sta = 0
        self.old_news = self.findById(segs_unit['_id'])
        if self.old_news:
            print("segs exists")
            return 1
        else:
            try:
                sta = self.opt_OnMySql.exeUpdate("insert into segs (_id,segments) values\
                 ('"+segs_unit["_id"]+"','"+segs_unit["segments"]+"')")
                if sta == 1:
                    print("insert segs success!")
            except:
                    print("insert failed!")
                    print("the word count is :"+ str(len(segs_unit["segments"])))
                    for i,k in segs_unit.items():
                        print(i)
                        print(k)
        # sta = self.opt_OnMySql.exeUpdate("insert into test (id,title) values(%d"%(int(news_unit["id"]))+",'"+news_unit["title"]+"')")
        return sta

    def deleteById(self,id):
        sta = self.opt_OnMySql.exeDeleteById("delete from segs where id='"+id+"'")
        return sta

    def deleteByIds(self,ids):
        sta = 0
        for eachID in ids:
            sta += self.deleteById(eachID)
        return sta

    def connClose(self):
        '''
            description:
                close the connection()
        '''
        self.opt_OnMySql.connClose()

if __name__ == "__main__":
    segsunit = SegsUnit().segs_unit
    segsunit["_id"] = "test"
    segsunit["segments"] = "一,二,三,四,五,六,七,八"
    print(segsunit)
    opt_segs = SegsOnMysql()
    opt_segs.insertOneSegs(segsunit)
    a = opt_segs.findall()
    for i in a:
        print(i[1].split(','))
    opt_segs.connClose()
