#coding=utf-8
import pymysql
import sys
from NewsUnit import *
reload(sys)
sys.setdefaultencoding('utf8')
class OptOnMysql(object):

    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_passowrd = "1234"
        self.db_name = "sina_news"
        try:
            self.conn = pymysql.connect(host=self.db_host,user=self.db_user,passwd=self.db_passowrd,db=self.db_name,charset='utf8')
            self.cur = self.conn.cursor()
            print("connect %s %s success"%(self.conn,self.cur))
        except:
            print("connect %s %s fail"%(self.conn,self.cur))
        #-----------------********************-----------------#
    def exeUpdate(self,sql):
        sta = self.cur.execute(sql)
        self.conn.commit()
        return (sta)

    def exeDeleteById(self,sql,ID):
        sta = 0
        sta = self.cur.execute(sql%(int(ID)))
        return(sta)

    def exeQuery(self,sql):
        self.cur.execute(sql)
        return(self.cur)

    def connClose(self):
        self.cur.close()
        self.conn.close()


class NewsOnMysql(object):
    def __init__(self):
        self.opt_OnMySql = OptOnMysql()

    def findById(self,id):
        cur = self.opt_OnMySql.exeQuery("select * from news where id = %d"%int(id))
        it = cur.fetchone()
        # print(it)
        if it == None:
            print("there is nothing found")
            return it
        else:
            print(it)
            return it
        # len_it = len(it)
        # if len_it==0:
        #     print("there is nothing found.")
        #     return 0
        # else:
        #     print(it)
        #     return 1

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
        # self.opt.db_user_unit.news_unit = news_unit
        sta = self.opt_OnMySql.exeUpdate("insert into news (id,title,content,time)values\
        (%d"%(int(news_unit["id"]))+",'"+news_unit["title"]+"','"+news_unit["content"]+"','"+news_unit["time"]+"')")
        if sta == 0:
            print("insert success!")
        else:
            print("insert failed!")
        # sta = self.opt_OnMySql.exeUpdate("insert into test (id,title) values(%d"%(int(news_unit["id"]))+",'"+news_unit["title"]+"')")
        return sta

    def deleteById(self,id):
        sta = self.opt_OnMySql.exeDeleteById("delete from news where id=%d",id)
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
    news_unit["id"] = 3
    news_unit["title"] = "今日说法"
    news_unit["content"] = "这是一个测试"
    news_unit["time"] = "20161202"
    opt = NewsOnMysql()
    # opt.findById(3)
    opt.findall()
    # cur = opt.findById(id)
    opt.connClose()
    # sta = opt.insertOneNews(news_unit)
    # print(sta)
