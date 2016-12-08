#coding=utf-8
import pymysql
from optOnMysql import *
from NewsUnit import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class NewsOnMysql(object):
    def __init__(self):
        self.opt_OnMySql = OptOnMysql()

    def findById(self,id):
        cur = self.opt_OnMySql.exeQuery("select * from news where _id = '"+id+"'")
        it = cur.fetchone()
        # print(it)
        if it == None:
            print("there is nothing found")
            return 0
        else:
            print(it)
            return 1

    def findall(self):
        cur = self.opt_OnMySql.exeQuery("select * from news")
        it = cur.fetchall()
        if it == None:
            print("this is now data")
            return it
        else:
            print("fetch all data")
            return it

    def insertOneNews(self,news_unit):
        '''
            description:
                 insert one news into mysql
            input:
                news_unit:
                    dict of news to be inserted
            output:
                num of insert news
        '''
        print("++++++++++++++++++8+++++++++++++++++++++")
        # self.opt.db_user_unit.news_unit = news_unit
        print("in insertOneNews")

        self.old_news = self.findById(news_unit['_id'])
        print("++++++++++++++++++9+++++++++++++++++++++")
        if self.old_news:
            print("news exists")
            return 1
        else:
            try:
                print("++++++++++++++++++10+++++++++++++++++++++")
                sta = self.opt_OnMySql.exeUpdate("insert into news (_id,title,content,time,category)values\
                 ('"+news_unit["_id"]+"','"+news_unit["title"]+"','"+news_unit["content"]+"','"+news_unit["time"]+"','"+news_unit["category"]+"')")
                print("++++++++++++++++++11+++++++++++++++++++++")
                if sta == 1:
                    print("insert success!")
                    print("++++++++++++++++++12+++++++++++++++++++++")
            except:
                    print("insert failed!")
                    print("the content length is :"+ str(len(news_unit["content"])))
                    for i,k in news_unit.items():
                        print(i)
                        print(k)
        # sta = self.opt_OnMySql.exeUpdate("insert into test (id,title) values(%d"%(int(news_unit["id"]))+",'"+news_unit["title"]+"')")
        return sta

    def deleteById(self,id):
        sta = self.opt_OnMySql.exeDeleteById("delete from news where id='%s'"%id)
        return sta

    def deleteByIds(self,ids):
        sta = 0
        for eachID in ids:
            sta += self.deleteById(eachID)
        return sta

    def connClose(self):
        self.opt_OnMySql.connClose()

if __name__ == "__main__":
    news_unit = dict()
    news_unit["_id"] = "asd"
    news_unit["title"] = "今日说法"
    news_unit["content"] = "这是一个测试"
    news_unit["time"] = "20161202"
    news_unit["category"] = "金融"
    # print(news_unit)
    opt = NewsOnMysql()
    # opt.insertOneNews(news_unit)
    opt.findById("doc-ifxyiayq2519635.shtml")
    # a = opt.findall()
    # for i in a :
        # print(i)
    opt.connClose()
